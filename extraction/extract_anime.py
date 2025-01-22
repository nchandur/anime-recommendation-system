import re
import requests
from bs4 import BeautifulSoup

def extract_number(text:str) -> int:
    m = re.search(r'\d{1,}', text)

    if m:
        return int(m.group().strip())
    
    return None


def get_names(soup:BeautifulSoup) -> dict:
    res = {
        "primary_name": "",
        "alternate_name": "",
    }

    names = soup.find("div", class_="h1 edit-info")
    res["primary_name"] = names.find("h1", class_="title-name h1_bold_none").text.strip()
    
    try:
        res["alternate_name"] = names.find("p", class_="title-english title-inherit").text.strip()
    except:
        pass

    return res

def get_stats(soup:BeautifulSoup) -> dict:
    res = {
        "score": 0.0,
        "vote_count": 0,
        "ranked": 0,
        "popularity": 0,
        "members": 0
    }
    
    stats = soup.find("div", class_="stats-block po-r clearfix")

    score = stats.find("div", class_="fl-l score")

    res["score"] = float(score.text.strip())
    res["vote_count"] = int(score.get("data-user").replace(",", "").replace("users", "").strip())

    others = stats.find("div", class_="di-ib ml12 pl20 pt8")

    res["ranked"] = others.find("span", class_="numbers ranked").text.strip()
    res["ranked"] = extract_number(res["ranked"])

    res["popularity"] = others.find("span", class_="numbers popularity").text.strip()
    res["popularity"] = extract_number(res["popularity"])

    res["members"] = others.find("span", class_="numbers members").text.replace(",", "").strip()
    res["members"] = extract_number(res["members"])

    return res
    
def get_information(soup:BeautifulSoup) -> dict:
    res = {
        "type": "",
        "episodes": 0,
        "status": "",
        "aired": "",
        "premiered": "",
        "producers" : [],
        "studios": [],
        "source": "",
        "genres": [],
        "themes": [],
        "demographic": [],
        "duration": "",
        "rating": ""
    }

    div = soup.find("div", class_="leftside")

    smalls = div.find_all("div", class_="spaceit_pad")

    for small in smalls:
        text = small.text

        m = re.search(r'Type:\n(.+)', text)
        if m:
            res["type"] = m.group(1).strip()

        m = re.search(r'Episodes:\n(.+)', text)
        if m:
            res["episodes"] = m.group(1).strip()

        m = re.search(r'Status:\n(.+)', text)
        if m:
            res["status"] = m.group(1).strip()

        m = re.search(r'Aired:\n(.+)', text)
        if m:
            res["aired"] = m.group(1).strip()

        m = re.search(r'Premiered:\n(.+)', text)
        if m:
            res["premiered"] = m.group(1).strip()

        m = re.search(r'Producers:\n(.+)', text)
        if m:
            res["producers"] = m.group(1).strip()
            res["producers"] = [ele.strip() for ele in res["producers"].split(", ")]

        m = re.search(r'Studios:\n(.+)', text)
        if m:
            res["studios"] = m.group(1).strip()
            res["studios"] = [ele.strip() for ele in res["studios"].split(", ")]

        m = re.search(r'Genres:\n(.+)', text)
        if m:
            res["genres"] = [ele.text.strip() for ele in small.find_all("a")]

        m = re.search(r'Themes:\n(.+)', text)
        if m:
            res["themes"] = [ele.text.strip() for ele in small.find_all("a")]

        m = re.search(r'Demographic:\n(.+)', text)
        if m:
            res["demographic"] = [ele.text.strip() for ele in small.find_all("a")]

        m = re.search(r'Duration:\n(.+)', text)
        if m:
            res["duration"] = m.group(1).strip()

        m = re.search(r'Rating:\n(.+)', text)
        if m:
            res["rating"] = m.group(1).strip()


    return res

def get_synopsis(soup:BeautifulSoup) -> str:
    text = soup.find("p", itemprop="description").text
    return text.strip()


def get_anime(url:str) -> dict:

    r = requests.get(url=url)

    if r.status_code != 200:
        return dict()

    soup = BeautifulSoup(r.text, "html.parser")

    try:

        res = get_names(soup=soup)
        res.update(get_stats(soup=soup))
        res.update(get_information(soup=soup))
        res["synopsis"] = get_synopsis(soup=soup)
        return res

    except:
        
        return dict()