import requests
import argparse
import os
import uuid
from client_configuration import CConfig


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP to the Equation server")
    parser.add_argument("path", help="Path to the image to solve")
    return parser.parse_args()


def make_request(ip, img_path):
    url = f"http://{ip}/equation?format_type=file&get_thumb=false"
    file = {'img1': open(img_path, 'rb')}
    return requests.post(url=url, files=file)


def download_request(response, config):

    if response.status_code == 200:
        image = os.path.join(config.images_path, f"{str(uuid.uuid4())}.jpeg")
        with open(image, "wb") as f:
            for stream in response.iter_content(1024):
                f.write(stream)

        print(f"200 | Path: {image}")
    else:
        print(response.content)


def main():
    arguments = parse_arguments()
    config = CConfig()
    download_request(make_request(arguments.ip, arguments.path), config)


if __name__ == "__main__":
    main()

