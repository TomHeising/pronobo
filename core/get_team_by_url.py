import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_url():
    # url = input("Please enter a URL: ")
    # url = "https://www.eurosport.fr/football/ligue-1/2023-2024/paris-saint-germain-toulouse-fc_mtc1447484/live.shtml"
    # url = "https://www.eurosport.fr/football/ligue-1/2023-2024/live-ogc-nice-le-havre-ac_mtc1447480/live.shtml"
    # url = "https://www.eurosport.fr/football/ligue-1/2023-2024/nantes-lille-osc_mtc1447485/live.shtml"
    url = "https://www.eurosport.fr/football/ligue-1/2023-2024/live-stade-brestois-stade-de-reims_mtc1447478/live.shtml"
    return url

def scrape_url_for_date(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    }

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    dates = soup.select("div.caps-s7-rs")  # Assuming there are multiple date elements with the class "caps-s7-rs"

    if dates:  # Check if any date elements were found
        date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'

        for date in dates:
            match = re.search(date_pattern, date.text)
            if match:
                # Extract the matched date
                extracted_date = match.group()
                return extracted_date  # Return the first matched date

    else:
        print("No date found on the webpage.")
        return None

def covert_string_into_date(string):

    date_format = "%d.%m.%Y"

    date_object = datetime.strptime(string, date_format)

    date_only = date_object.date()

    return date_only


def get_team_names(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    }

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    name_team1 = soup.select('div.overflow-hidden')[35]
    name_team2 = soup.select('div.overflow-hidden')[36]

    teams = []
    teams.append(name_team1.text)
    teams.append(name_team2.text)


    return teams

def get_ligue(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    }

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    ligue = soup.select('div.caps-s7-rs')[0]
    ligue_name = ligue.text.split("/")[0].rstrip()

    return ligue_name

def get_datas():

    url = get_url()
    date = scrape_url_for_date(url)
    real_date = covert_string_into_date(date)
    team_names = get_team_names(url)
    ligue_name = get_ligue(url)
    
    return ligue_name, real_date, team_names


    

