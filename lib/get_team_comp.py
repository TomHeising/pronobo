from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_team_comp(url):
    # Obtenez le contenu HTML de la page
    html_data = requests.get(url).text

    # Créez un objet BeautifulSoup
    soup = BeautifulSoup(html_data, "html.parser")

    # Récupérer les noms des deux équipes
    team_names = [team.text.strip() for team in soup.find_all('div', attrs={"class": "overflow-hidden text-ellipsis"}, limit=2)]
    # Récupérer les blocs de composition des équipes
    compo_blocks = soup.find_all('div', class_='zone-section-margin--top-small')

    # Initialisation des listes pour les compositions des équipes
    equipe1_players = []
    equipe2_players = []
    if len(compo_blocks) != 0:
        # Parcourir les blocs de composition
        for block in compo_blocks:
            # Récupérer les noms des joueurs pour l'équipe 1
            players_team1 = block.find_all('ul')[0].find_all('a', class_='truncate')
            players_team1_names = [re.search(r'/football/([\w-]+)_prs', player['href']).group(1).replace('-', ' ') for player in players_team1]

            # Ajouter les joueurs à la liste de l'équipe 1
            equipe1_players.extend(players_team1_names)

            # Récupérer les noms des joueurs pour l'équipe 2
            players_team2 = block.find_all('ul')[1].find_all('a', class_='truncate')
            players_team2_names = [re.search(r'/football/([\w-]+)_prs', player['href']).group(1).replace('-', ' ') for player in players_team2]

            # Ajouter les joueurs à la liste de l'équipe 2
            equipe2_players.extend(players_team2_names)

        return team_names, [equipe1_players, equipe2_players]
    
    else:
        url = url.replace("/live.shtml", "/live-lineup.shtml")

        html_data = requests.get(url).text

        # Créez un objet BeautifulSoup
        soup = BeautifulSoup(html_data, "html.parser")

        compo_blocks = soup.find_all('div', class_='zone-section-margin--top-small')  

        if len(compo_blocks) >= 2:

            for block in compo_blocks[1:-1]:
                print("ahaha")
                players_team1= block.find_all('ul')[0].find_all('a', class_='truncate')
                players_team1_names = [re.search(r'/football/([\w-]+)_prs', player['href']).group(1).replace('-', ' ') for player in players_team1]

                equipe1_players.extend(players_team1_names)

                players_team2 = block.find_all('ul')[1].find_all('a', class_='truncate')
                players_team2_names = [re.search(r'/football/([\w-]+)_prs', player['href']).group(1).replace('-', ' ') for player in players_team2]

                # Ajouter les joueurs à la liste de l'équipe 2
                equipe2_players.extend(players_team2_names)
            
            return team_names, [equipe1_players, equipe2_players]


    