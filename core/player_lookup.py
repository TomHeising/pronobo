from bs4 import BeautifulSoup
import json
import requests

def get_overall_score(name, team_name, iteration):

    html_data = requests.get("https://www.ea.com/games/ea-sports-fc/ratings?search=" + name).text

    soup = BeautifulSoup(html_data, "html.parser")
    script_content = soup.find("script", {"id": "__NEXT_DATA__"}).string

    data = json.loads(script_content)

    player_score = None

    for player_data in data["props"]["pageProps"]["ratingsEntries"]["items"]:
        player_full_name = f"{player_data['firstName']} {player_data['lastName']}"
        player_team = player_data["team"]["label"]
        player_score = player_data["overallRating"]
        if player_team == team_name:
            break 

    if player_score is None:
        n_name = ""
        if iteration == 0:
            names = name.split()
            if len(names) > 2:
                n_name = " ".join(names[:2])
            else:
                n_name = " ".join(names)
        elif iteration == 1:
            n_name = name.split()[1]
        
        return get_overall_score(n_name, team_name, iteration + 1)
    else:
        return player_score