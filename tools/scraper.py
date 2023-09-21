import os
import sys
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from PIL import Image
import time


crawler = BingImageCrawler(
    downloader_threads=1, storage={"root_dir": "."})


def crop_and_resize(filepath, outfilepath, size=128):
    with Image.open(filepath) as img:
        width, height = img.size
        min_dimension = min(width, height)
        left = (width - min_dimension) / 2
        top = (height - min_dimension) / 2
        right = (width + min_dimension) / 2
        bottom = (height + min_dimension) / 2
        img_cropped = img.crop((left, top, right, bottom))
        img_resized = img_cropped.resize((size, size))
        img_resized.save(outfilepath)


def get_first_image(query, query2):
    query = query.replace("'", " ")
    query = query.replace(",", " ")
    query = query.replace("-", "")
    query = query.replace("  ", " ")
    search_filters = dict()  # layout="square")
    crawler.crawl(query + " " + query2,
                  filters=search_filters, max_num=1)
    time.sleep(3)
    crop_and_resize("000001.jpg", query + ".jpg")
    os.remove("000001.jpg")


def process_mp3(file_path, user_query):
    query = os.path.splitext(file_path)[0]
    image_url = get_first_image(query, user_query)
    if image_url:
        print(f"Nom du fichier MP3 : {query}")
        print(f"URL de la première image Google : {image_url}")
    else:
        print(f"Aucune image trouvée pour : {query}")


def main(directory, user_query):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                process_mp3(file, user_query)


if __name__ == "__main__":
    directory = sys.argv[1]
    user_query = "marlene jobert site:amazon.fr"
    if len(sys.argv) > 2:
        user_query = sys.argv[2]
    main(directory, user_query)
