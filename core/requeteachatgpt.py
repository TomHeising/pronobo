import requests
import pandas as pd
from collections import defaultdict
import json

class FootballDataAPI:
    BASE_URL = "https://api.football-data.org/v2/"
    COMPETITIONS = {2021: "Premier League", 2015: "Ligue 1", 2014: "La Liga", 2002: "Bundesliga", 2019: "Serie A"}
    HEADERS = {"X-Auth-Token": "35d0c66545244cb0803d3e5ac94fb539"} # Replace with your actual API token

    @classmethod
    def get_matches(cls, start_date, end_date):
        matches = []
        for competition_id, competition_name in cls.COMPETITIONS.items():
            matches.extend(cls._fetch_matches_for_competition(competition_id, competition_name, start_date, end_date))
        return matches

    @classmethod
    def _fetch_matches_for_competition(cls, competition_id, competition_name, start_date, end_date):
        url = f"{cls.BASE_URL}competitions/{competition_id}/matches?dateFrom={start_date}&dateTo={end_date}"
        response = requests.get(url, headers=cls.HEADERS)
        if response.status_code == 200:
            matches_data = response.json()["matches"]
            for match in matches_data:
                match["competitionName"] = competition_name
            return matches_data
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response text: {response.text}")
            return []

# Add your team name mapping here
TEAM_NAPS = {
"Burnley FC": "Burnley",
"Manchester City FC": "Manchester City",
"Arsenal FC": "Arsenal",
"Nottingham Forest FC": "Nottingham Forest",
"AFC Bournemouth": "Bournemouth",
"West Ham United FC": "West Ham",
"Brighton & Hove Albion FC": "Brighton & Hove Albion",
"Luton Town FC": "Luton Town",
"Everton FC": "Everton",
"Fulham FC": "Fulham",
"Sheffield United FC": "Sheffield United",
"Crystal Palace FC": "Crystal Palace",
"Newcastle United FC": "Newcastle",
"Aston Villa FC": "Aston Villa",
"Brentford FC": "Brentford",
"Tottenham Hotspur FC": "Tottenham",
"Chelsea FC": "Chelsea",
"Liverpool FC": "Liverpool",
"Manchester United FC": "Manchester United",
"Wolverhampton Wanderers FC": "Wolverhampton",
"OGC Nice": "OGC Nice",
"Lille OSC": "Lille OSC",
"Olympique de Marseille": "Olympique de Marseille",
"Stade de Reims": "Stade de Reims",
"Paris Saint-Germain FC": "Paris Saint-Germain",
"FC Lorient": "FC Lorient",
"Stade Brestois 29": "Stade Brestois",
"Racing Club de Lens": "RC Lens",
"Clermont Foot 63": "Clermont Foot",
"AS Monaco FC": "Monaco",
"FC Nantes": "Nantes",
"Toulouse FC": "Toulouse FC",
"Montpellier HSC": "Montpellier Hérault",
"Le Havre AC": "Le Havre AC",
"Stade Rennais FC 1901": "Stade Rennais",
"FC Metz": "Metz",
"RC Strasbourg Alsace": "Strasbourg",
"Olympique Lyonnais": "Olympique Lyonnais",
"UD Almería": "UD Almería",
"Rayo Vallecano de Madrid": "Rayo Vallecano",
"Sevilla FC": "FC Séville",
"Valencia CF": "Valence",
"Real Sociedad de Fútbol": "Real Sociedad",
"Girona FC": "Girona FC",
"UD Las Palmas": "UD Las Palmas",
"RCD Mallorca": "Majorque",
"Athletic Club": "Athletic Club",
"Real Madrid CF": "Real Madrid",
"RC Celta de Vigo": "Celta Vigo",
"CA Osasuna": "CA Osasuna",
"Villarreal CF": "Villarreal",
"Real Betis Balompié": "Betis Séville",
"Getafe CF": "Getafe CF",
"FC Barcelona": "FC Barcelone",
"Cádiz CF": "Cadix",
"Deportivo Alavés": "Deportivo Alavés",
"Club Atlético de Madrid": "Atlético Madrid",
"Granada CF": "Granada CF",
"SV Werder Bremen": "Werder Brême",
"FC Bayern München": "Bayern Munich",
"Bayer 04 Leverkusen": "Bayer 04 Leverkusen",
"RB Leipzig": "RB Leipzig",
"VfL Wolfsburg": "Wolfsburg",
"FC Heidenheim 1846": "FC Heidenheim",
"TSG 1899 Hoffenheim": "TSG Hoffenheim",
"SC Freiburg": "Fribourg",
"FC Augsburg": "FC Augsburg",
"Borussia Mönchengladbach": "Mönchengladbach",
"VfB Stuttgart": "Stuttgart",
"VfL Bochum 1848": "Bochum",
"Borussia Dortmund": "Dortmund",
"FC Köln": "Cologne",
"FC Union Berlin": "FC Union Berlin",
"FSV Mainz 05": "Mayence",
"Eintracht Frankfurt": "Eintracht Francfort",
"SV Darmstadt 98": "SV Darmstadt 98",
"Empoli FC" : "EMPOLI",
"Hellas Verona FC":"Hellas Verona",
"Frosinone Calcio":"Frosinone",
"SSC Napoli":"Naples",
"Genoa CFC":"Genoa",
"ACF Fiorentina":"Fiorentina",
"AC Monza":"Monza",
"AS Roma":"AS Rome",
"US Salernitana 1919":"Salernitana",
"US Sassuolo Calcio":"Sassuolo",
"Atalanta BC":"Atalanta",
"US Lecce":"Lecce",
"SS Lazio":"Lazio Rome",
"Udinese Calcio":"Udinese",
"Juventus FC":"Juventus Turin",
"Torino FC":"Torino",
"Cagliari Calcio":"Cagliari",
"Bologna FC 1909":"Bologne",
"AC Milan":"AC Milan",
}

def process_matches(matches):
    stats_data = defaultdict(lambda: defaultdict(int))
    for match in matches:
        if match["score"]["fullTime"]["homeTeam"] is not None and match["score"]["fullTime"]["awayTeam"] is not None:
            update_stats(stats_data, match)
    return stats_data

def update_stats(stats_data, match):
    home_team = TEAM_NAPS.get(match["homeTeam"]["name"], match["homeTeam"]["name"])
    away_team = TEAM_NAPS.get(match["awayTeam"]["name"], match["awayTeam"]["name"])
    home_goals = match["score"]["fullTime"]["homeTeam"]
    away_goals = match["score"]["fullTime"]["awayTeam"]

    stats_data[home_team]["HomeGoalsScored"] += home_goals
    stats_data[home_team]["HomeGoalsConceded"] += away_goals
    stats_data[away_team]["AwayGoalsScored"] += away_goals
    stats_data[away_team]["AwayGoalsConceded"] += home_goals

    if home_goals > away_goals:
        stats_data[home_team]["HomeWins"] += 1
        stats_data[away_team]["AwayLosses"] += 1
    elif home_goals < away_goals:
        stats_data[home_team]["HomeLosses"] += 1
        stats_data[away_team]["AwayWins"] += 1
    else:  # home_goals == away_goals
        stats_data[home_team]["HomeDraws"] += 1
        stats_data[away_team]["AwayDraws"] += 1

def main():
    start_date = "2023-08-11"
    end_date = "2024-03-18"
    matches = FootballDataAPI.get_matches(start_date, end_date)
    stats_data = process_matches(matches)
    stats_list = []
    for team, stats in stats_data.items():
        stats["Team"] = team
        stats_list.append(stats)
    with open("stats_data.json", "w") as f:
        json.dump(stats_list, f, indent=4)
    print("Stats data successfully written to stats_data.json")

if __name__ == "__main__":
    main()