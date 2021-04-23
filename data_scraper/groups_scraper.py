from data_scraper.constants import *
from bs4 import BeautifulSoup
import requests
import re
import json


def save_data(json_file):
    res = {}
    groups = import_groups()
    for group in groups:
        group_id = group[0]
        group_name = group[1]
        techniques = extract_group_detail(group_id)
        for technique in techniques:
            id1 = group_name + "//" + group_id + "//" + technique[1]
            res[id1] = technique[0]
    exploits = import_exploits()
    for exploit in exploits:
        exploit_id = exploit[0]
        exploit_name = exploit[1]
        techniques = extract_exploit_detail(exploit_id)
        for technique in techniques:
            id1 = exploit_name + "//" + exploit_id + "//" + technique[1]
            res[id1] = technique[0]
    with open(json_file, "w") as f:
        json.dump(res, f, indent=2)
    return 0


def import_groups():
    res = []
    try:
        response = requests.get(GROUPS_ADDRESS)
    except:
        print(f"Error Reading {GROUPS_ADDRESS}")
        return res

    if response.status_code != 200:
        print(f"Error Reading {GROUPS_ADDRESS}")
        return res
    soup = BeautifulSoup(response.text, "html.parser")
    for div_temp in soup.find_all("div", {"class": "sidenav"}):
        sp = BeautifulSoup(str(div_temp), "html.parser")
        for link in sp.find_all("a"):
            id1 = re.sub("[\\s+\\/]", "", re.sub("groups", "", link.get("href")))
            name = re.sub("\\s+", "", link.text)
            if id1 != "":
                if [id1, name] not in res:
                    res.append([id1, name])
    return res


def import_exploits():
    res = []
    try:
        response = requests.get(EXPLOITS_ADDRESS)
    except:
        print(f"Error Reading {EXPLOITS_ADDRESS}")
        return res

    if response.status_code != 200:
        print(f"Error Reading {EXPLOITS_ADDRESS}")
        return res
    soup = BeautifulSoup(response.text, "html.parser")
    for div_temp in soup.find_all("div", {"class": "sidenav"}):
        sp = BeautifulSoup(str(div_temp), "html.parser")
        for link in sp.find_all("a"):
            id1 = re.sub("[\\s+\\/]", "", re.sub("software", "", link.get("href")))
            name = re.sub("\\s+", "", link.text)
            if id1 != "":
                if [id1, name] not in res:
                    res.append([id1, name])
    return res


def extract_group_detail(group_id):
    res = []
    address = GROUPS_ADDRESS + group_id
    try:
        response = requests.get(address)
    except:
        print(f"Error Reading {address}")
        return res
    if response.status_code != 200:
        print(f"Error Reading {address}")
        return res
    soup = BeautifulSoup(response.text, "html.parser")
    table_str = str(soup.find("table", {"class": "table techniques-used table-bordered mt-2"}))
    soup = BeautifulSoup(table_str, "html.parser")
    for tr_temp in soup.find_all("tr"):
        sp = BeautifulSoup(str(tr_temp), "html.parser")
        id1 = ""
        for link in sp.find_all("a"):
            href = link.text
            if re.match("T[0-9]+", href, re.IGNORECASE):
                id1 += href
            elif re.match("\\.[0-9]+", href, re.IGNORECASE):
                if id1 != "":
                    id1 += href
                else:
                    txt = link.get("href")
                    id1 = re.sub("/", ".", re.sub("/techniques/", "", txt))
            else:
                pass
        for par in sp.find_all("p"):
            text = BeautifulSoup(str(par), "html.parser").text
            if text != "" and id1 != "":
                res.append((text, id1))
    return res


def extract_exploit_detail(exploit_id):
    res = []
    address = EXPLOITS_ADDRESS + exploit_id
    try:
        response = requests.get(address)
    except:
        print(f"Error Reading {address}")
        return res
    if response.status_code != 200:
        print(f"Error Reading {address}")
        return res
    soup = BeautifulSoup(response.text, "html.parser")
    table_str = str(soup.find("table", {"class": "table techniques-used table-bordered mt-2"}))
    soup = BeautifulSoup(table_str, "html.parser")
    for tr_temp in soup.find_all("tr"):
        sp = BeautifulSoup(str(tr_temp), "html.parser")
        id1 = ""
        for link in sp.find_all("a"):
            href = link.text
            if re.match("T[0-9]+", href, re.IGNORECASE):
                id1 += href
            elif re.match("\\.[0-9]+", href, re.IGNORECASE):
                if id1 != "":
                    id1 += href
                else:
                    txt = link.get("href")
                    id1 = re.sub("/", ".", re.sub("/techniques/", "", txt))
            else:
                pass
        for par in sp.find_all("p"):
            text = BeautifulSoup(str(par), "html.parser").text
            if text != "" and id1 != "":
                val = text
                res.append((text, id1))
    return res


if __name__ == "__main__":
    res1 = save_data("C:\\Users\\Igor\\Projects\\anvilogic\\test\\model_data.json")
