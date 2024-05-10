import requests
import pandas as pd
from collections import defaultdict
import json

class FootballDataAPI:
    BASE_URL = "https://api.football-data.org/v2/"
    COMPETITIONS = {2021: "Premier League", 2015: "Ligue 1", 2014: "La Liga", 2002: "Bundesliga", 2019: "Serie A", 2001: "Champions League"}  # Add Champions League
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

def process_matches(matches):
    stats_data = defaultdict(lambda: defaultdict(int))
    for match in matches:
        if match["score"]["fullTime"]["homeTeam"] is not None and match["score"]["fullTime"]["awayTeam"] is not None:
            update_stats(stats_data, match)
    return stats_data

def update_stats(stats_data, match):
    home_team = match["homeTeam"]["name"]
    away_team = match["awayTeam"]["name"]
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
    end_date = "2024-02-12"
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