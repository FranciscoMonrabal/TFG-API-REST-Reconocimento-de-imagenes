import requests
import argparse


def parse_arguments():
    pass


def make_request(ip, img_path):
    url = "http://127.0.0.1:5000/predict?format_type=file&get_thumb=false"
    file = {'img1': open('image0.jpg', 'rb')}
    response = requests.post(url=url, files=file)
    print(response.text)


def main():
    pass


if __name__ == "__main__":
    main()

    