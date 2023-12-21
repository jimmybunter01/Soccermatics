import requests
import os
from tqdm import tqdm

def check_for_data_dir():
    cwd = os.getcwd()
    if 'data' not in os.listdir(cwd):
        print("No data directory! Creating it!")
        try: 
            os.mkdir(f"{cwd}\\data\\wyscout")
            print("Data Directory Made!")
        except Exception as e:
            print(f"Directory could not be made due  to - {e}")

    if 'wyscout' not in os.listdir(f"{cwd}\\data"):
        try: 
            os.mkdir(f"{cwd}\\data\\wyscout")
            print("Wyscout Directory Made!")
        except Exception as e:
            print(f"Directory could not be made due  to - {e}")


def main():
    article_ids = []
    wyscout_collection_url = "https://api.figshare.com/v2/collections/4415000/articles"
    download_urls = {}

    check_for_data_dir()

    api_response = requests.get(wyscout_collection_url)
    for article in api_response.json():
        if article["defined_type_name"] == "dataset":
            article_ids.append(article["id"])

    for article_id in article_ids:
        wyscout_article_url = f"https://api.figshare.com/v2/articles/{article_id}"
        api_response = requests.get(wyscout_article_url)
        dataset_details = api_response.json()["files"][0]
        dataset_name = dataset_details["name"]
        download_urls[dataset_name] = dataset_details["download_url"]

    for file, url in tqdm(download_urls.items()):
        file_request = requests.get(url)
        open(f"data/wyscout/{file}", "wb").write(file_request.content)


if __name__ == "__main__":
    main()
