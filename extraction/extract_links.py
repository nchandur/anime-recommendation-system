import requests
from random import randint
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup

def extract_links(topK:int=0) -> list[str]:
    base = "https://myanimelist.net/topanime.php?limit={}".format(topK)

    r = requests.get(url=base)

    soup = BeautifulSoup(r.text, "html.parser")

    div = soup.find("div", class_="pb12")
    tds = div.find_all("td", class_="title al va-t word-break")

    links = [td.find("a").get("href") for td in tds]

    return links

all_links = []

for i in tqdm(range(0, 2000, 50)):
    links = extract_links(topK=i)
    all_links += links
    sleep(randint(10, 20))

with open("data/links.txt", "w") as file:
    for link in all_links:
        file.write("{}\n".format(link))