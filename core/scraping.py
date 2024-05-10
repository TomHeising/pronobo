years = list(range(2024, 2023, -1))


competitions_url = ["https://fbref.com/en/comps/9/Premier-League-Stats","https://fbref.com/en/comps/20/Bundesliga-Stats","https://fbref.com/en/comps/13/Ligue-1-Stats","https://fbref.com/en/comps/12/La-Liga-Stats","https://fbref.com/en/comps/11/Serie-A-Stats"]



import requests
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
}

for comp in competitions_url:
    
    all_matches = []
    all_np_matches = []
    standings_url=comp
    competition_name = comp.split("/")[-1].replace("-Stats", "").replace("-", " ")
    
    for year in years:
        data = requests.get(standings_url, headers = headers)
        soup = BeautifulSoup(data.text)
        standings_table = soup.select('table.stats_table')[0]
    
        links = [l.get("href") for l in standings_table.find_all('a')]
        links = [l for l in links if '/squads/' in l]
        team_urls = [f"https://fbref.com{l}" for l in links]
        
        previous_season = soup.select("a.prev")[0].get("href")
        standings_url = f"https://fbref.com{previous_season}"
        
        for team_url in team_urls:
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
            data = requests.get(team_url)
            matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures")[0]
    
            np_matches = matches.loc[matches["Result"].isna()] 
            
            soup = BeautifulSoup(data.text)
            links = [l.get("href") for l in soup.find_all('a')]
            links = [l for l in links if l and 'all_comps/shooting/' in l]
            data = requests.get(f"https://fbref.com{links[0]}")
            
            shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()
            
            try:
                team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
                
            except ValueError:
                continue
                
            team_data = team_data[team_data["Comp"] == competition_name]
            np_matches = np_matches[np_matches["Comp"] == competition_name]
            
            team_data["Season"] = year
            team_data["Team"] = team_name
            all_matches.append(team_data)
            
            np_matches["Season"] = year
            np_matches["Team"] = team_name

            np_matches['Time'] = np.random.randint(17, 21, size=len(np_matches))
            shooting_st = ["Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
            np_matches[shooting_st] = np.nan
            
            all_np_matches.append(np_matches)
    
            time.sleep(4)

    competition_name = comp.split("/")[-1].replace("-Stats", "").replace("-", " ").replace(" ", "")
    
    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]
    match_df.to_csv("matches_" + competition_name + ".csv")
    np_match_df = pd.concat(all_np_matches)
    np_match_df.columns = [c.lower() for c in np_match_df.columns]
    np_match_df.to_csv("np_matches_" + competition_name + ".csv")
    
    