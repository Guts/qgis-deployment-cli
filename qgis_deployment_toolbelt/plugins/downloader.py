import concurrent.futures
import io
import zipfile

import requests

urls = [
    "http://mlg.ucd.ie/files/datasets/multiview_data_20130124.zip",
    "http://mlg.ucd.ie/files/datasets/movielists_20130821.zip",
    "http://mlg.ucd.ie/files/datasets/bbcsport.zip",
    "http://mlg.ucd.ie/files/datasets/movielists_20130821.zip",
    "http://mlg.ucd.ie/files/datasets/3sources.zip",
]


def download_zips(url):
    file_name = url.split("/")[-1]
    response = requests.get(url)
    sourceZip = zipfile.ZipFile(io.BytesIO(response.content))
    print("\n Downloaded {} ".format(file_name))
    sourceZip.extractall(filePath)
    print("extracted {} \n".format(file_name))
    sourceZip.close()


with concurrent.futures.ThreadPoolExecutor() as exector:
    exector.map(download_zip, urls)
