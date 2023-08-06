import argparse
import pathlib
import uuid
import tqdm
from ..common import Environment, ImageDownloader, get_image_size
from ..dataset import Dataset, DatasetWriter
from ..training_api import TrainingApi


def download_predictions(env, project_id, iteration_id, output_directory, probability_threshold=0):
    training_api = TrainingApi(env)
    domain_id = training_api.get_project(project_id)['domain_id']
    domain_type = training_api.get_domain(domain_id)['type']
    dataset = Dataset(domain_type, output_directory)

    tags = training_api.get_tags(project_id)
    tag_names, tag_ids = zip(*tags)
    dataset.labels = tag_names
    image_predictions = training_api.get_predictions(project_id, iteration_id)

    downloader = ImageDownloader()
    for entry in tqdm.tqdm(image_predictions, "Downloading images"):
        try:
            image = downloader.download_binary(entry['image_url'])
        except IOError as e:
            tqdm.write(f"Failed to download {entry['image_url']} due to {e}. Ignoring the error.")
            continue

        if domain_type == 'object_detection':
            image_size = get_image_size(image)
            labels = [[tag_ids.index(uuid.UUID(p['tagId'])),
                       max(int(p['boundingBox']['left'] * image_size[0]), 0),
                       max(int(p['boundingBox']['top'] * image_size[1]), 0),
                       min(int((p['boundingBox']['left'] + p['boundingBox']['width']) * image_size[0]), image_size[0]),
                       min(int((p['boundingBox']['top'] + p['boundingBox']['height']) * image_size[1]), image_size[1])] for p in entry['predictions'] if p['probability'] > probability_threshold]
        else:
            raise NotImplementedError("Classificaiton dataset is not supported yet.")
            labels = []

        dataset.add_data(image, labels)

    if len(dataset) == 128:
        print("WARNING: this command supports downloading only 128 images.")

    print(f"Downloaded {len(dataset)} images.")

    output_directory.mkdir(parents=True, exist_ok=True)
    DatasetWriter.write(dataset, output_directory / 'images.txt')
    print(f"Saved the dataset to {output_directory}")


def main():
    parser = argparse.ArgumentParser(description="Download stored prediction results")
    parser.add_argument('project_id', type=uuid.UUID)
    parser.add_argument('iteration_id', type=uuid.UUID)
    parser.add_argument('output_directory', type=pathlib.Path)
    parser.add_argument('--threshold', default=0.1, type=float, help="Probability threshold")

    args = parser.parse_args()

    if args.output_directory.exists():
        parser.error(f"{args.output_directory} already exists.")

    download_predictions(Environment(), args.project_id, args.iteration_id, args.output_directory, args.threshold)


if __name__ == '__main__':
    main()
