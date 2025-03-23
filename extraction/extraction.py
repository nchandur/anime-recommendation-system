import os
import pandas as pd
from tqdm import tqdm
from random import randint
from time import sleep
from extract_anime import get_anime

with open("data/links.txt") as file:
    links = file.readlines()

rows = []

with open("data/errors.csv", "w") as error:
    error.write("url, error\n")

    for link in tqdm(links[:]):
        
        try:

            anime = get_anime(link.strip())
            rows.append(anime)
            error.write("{}, None\n".format(link.strip()))
            sleep(randint(3, 7))

        except Exception as e:

            error.write("{}, {}\n".format(link.strip(), e.__class__))

data = pd.DataFrame(rows)

destination = "data/raw.csv"

if not os.path.isfile(destination):
    data.to_csv(destination, index=False)
else:
    data.to_csv(destination, mode="a", header=False, index=False)