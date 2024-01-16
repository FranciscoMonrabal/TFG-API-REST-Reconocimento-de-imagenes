import requests
import argparse
import os
import uuid


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP to the Equation server")
    parser.add_argument("path", help="Path to the image to solve")
    return parser.parse_args()


def make_request(ip, img_path):
    url = f"http://{ip}/equation?format_type=file&get_thumb=false"
    file = {'img1': open(img_path, 'rb')}
    return requests.post(url=url, files=file)


def download_request(response):

    if response.status_code != 500:
        with open(os.path.join(r"\images", str(uuid.uuid4()), "wb")) as f:
            for stream in response.iter_content(1024):
                f.write(stream)


def main():
    arguments = parse_arguments()
    download_request(make_request(arguments.ip, arguments.path))


if __name__ == "__main__":
    main()

