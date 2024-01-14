import requests
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP to the Equation server")
    parser.add_argument("path", help="Path to the image to solve")
    return parser.parse_args()


def make_request(ip, img_path):
    url = f"http://{ip}/predict?format_type=file&get_thumb=false"
    file = {'img1': open(img_path, 'rb')}
    return requests.post(url=url, files=file)


def main():
    arguments = parse_arguments()
    img = make_request(arguments.ip, arguments.path)




if __name__ == "__main__":
    main()

