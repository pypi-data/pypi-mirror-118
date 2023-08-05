
# image = Image.open('image.jpg')
# image.show()
#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from os import name, path, makedirs
from requests import get
from typing import Optional, Tuple
from PIL import Image
from io import BytesIO
from re import match


def get_comic(comic: Optional[int]) -> Tuple[str, Image.Image]:

    code = comic if comic else ""

    request = get(f"https://xkcd.com/{code}").text.strip()
    soup = BeautifulSoup(request, "html.parser")

    print("Title:", soup.find("div", {"id": "ctitle"}).text)

    comic = soup.find("div", {"id": "comic"})
    img = comic.find("img")

    print("Message:", img["title"])

    url = next(link for link in soup.findAll("a") if match('.*/xkcd.com/[0-9]*', link["href"]))["href"]
    print("URL:", url)

    content = get(f"https://{img['src'].lstrip('/')}").content
    image = Image.open(BytesIO(content))
    image.show()


def run():

    parser = ArgumentParser(prog="xkcd")
    parser.add_argument("--comic", type=int)

    namespace = parser.parse_args()
    get_comic(namespace.comic)


if __name__ == "__main__":
    run()
