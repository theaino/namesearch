import requests
import zipfile
import os
from os import path
from source import Name, Source
from io import StringIO, BytesIO
import csv


TMP = "tmp"


def get_cached(url, save):
    filepath = path.join(TMP, save)
    if path.isfile(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    os.makedirs(path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(response.content)
    return response.content


def fetch_usa():
    os.makedirs(TMP, exist_ok=True)

    url = "https://www.ssa.gov/oact/babynames/names.zip"
    data = get_cached(url, "usa.zip")

    extractpath = path.join(TMP, "usa")
    os.makedirs(extractpath, exist_ok=True)

    with zipfile.ZipFile(BytesIO(data), "r") as z:
        z.extractall(path=extractpath)

    result = {}
    for file in os.listdir(extractpath):
        filepath = path.join(extractpath, file)
        if not path.isfile:
            continue
        if not file.startswith("yob"):
            continue
        year = int(file.replace("yob", "").split(".")[0])
        with open(filepath, "r") as f:
            lines = f.read().strip().split("\n")
            result[year] = []
            for line in lines:
                parts = line.split(",")
                result[year].append(
                        Name(parts[0].lower(), parts[1], int(parts[2]))
                        )

    return result

def fetch_canada():
    urls = {
            "M": "https://www.donneesquebec.ca/recherche/dataset/93d640ec-d059-4768-b7ed-388604b278aa/resource/c35c6bc3-fbc1-47bd-bfa9-90be087f954a/download/gars1980-2023.csv",
            "F": "https://www.donneesquebec.ca/recherche/dataset/13db2583-427a-4e5f-b679-8532d3df571f/resource/e1f20072-935d-4a92-91c4-61a12fbe687b/download/filles1980-2023.csv"
            }

    result = {}
    for gender in urls.keys():
        url = urls[gender]
        data = get_cached(url, path.join("canada", f"{gender}.csv")).decode("utf-8")
        reader = csv.reader(StringIO(data), delimiter=",")
        y = -1
        header = []
        for row in reader:
            y += 1
            row = list(row)[:-1]
            if y == 0:
                header = row
                continue
            x = -1
            name = ""
            if row[0].endswith(":"):
                continue
            for column in row:
                x += 1
                if x == 0:
                    name = column.lower()
                    continue
                year = int(header[x])
                if year not in result:
                    result[year] = []
                result[year].append(Name(name, gender, int(column)))
    return result


SOURCES = [
        Source("usa", fetch_usa),
        Source("canada", fetch_canada)
        ]
