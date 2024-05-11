import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from lib.get_team_by_url import get_datas

import sqlite3

class MissingDict(dict):
    __missing__ = lambda self, key: key

#np_matches  = np_matches_un[(np_matches_un['team'] == home_team) & (np_matches_un['opponent'] == away_team)]

def rolling_averages(group, cols, new_cols):

    
    group = group.sort_values("date")

    if(group.shape[0 ] == 1):
        rolling_stats = group[cols].rolling(1, closed='left').mean()
    
    else : 
        rolling_stats = group[cols].rolling(3, closed='left').mean()
    
    group[new_cols] = rolling_stats
    
    #group = group.dropna(subset=new_cols)

    return group

def data_process(matches):

    del matches["comp"]
    del matches["round"]
    del matches["captain"]
    del matches["formation"]
    del matches["referee"]

    matches["date"] = pd.to_datetime(matches["date"])
    matches["target"] = (matches["result"] == "W").astype("int")
    matches["venue_code"] = matches["venue"].astype("category").cat.codes
    matches["opp_code"] = matches["opponent"].astype("category").cat.codes
    matches["time"] = matches["time"].astype(str)
    matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
    matches["day_code"] = matches["date"].dt.dayofweek


    cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
    new_cols = [f"{c}_rolling" for c in cols]

    matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
    matches_rolling = matches_rolling.droplevel('team') 
    

    return matches_rolling, new_cols

def make_predictions(matches,np_matches, new_cols, home_team, away_team):

    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

    predictors = ["venue_code", "opp_code", "hour", "day_code"]

    new_predictors = predictors + new_cols

    new_np_matches = np_matches
    new_np_matches = new_np_matches[(np_matches['team'] == away_team) & (np_matches['opponent'] == home_team)]

    np_matches  = np_matches[(np_matches['team'] == home_team) & (np_matches['opponent'] == away_team)]
    

    train = matches
    test = np_matches
    test_2 = new_np_matches


    rf.fit(train[new_predictors], train["target"])
    preds = rf.predict(test[new_predictors])
    other_preds = rf.predict(test_2[new_predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return preds,other_preds

def get_result(preds, other_pred, home_team, away_team, ligue_name, game_date, url):

    if preds:

        conn = sqlite3.connect('lib/data_results/results_db.db')
        cur = conn.cursor()

        data = (home_team, away_team, home_team, ligue_name, game_date, url)

        try:

            cur.execute("INSERT INTO results(home_team, away_team, win_team, ligue_name, date, url) VALUES(?, ?, ?, ?, ?, ?)", data)
            conn.commit()

            cur.close()
            conn.close()
            

        except sqlite3.IntegrityError:

            cur.close()
            conn.close()
    
    elif other_pred: 

        conn = sqlite3.connect('lib/data_results/results_db.db')
        cur = conn.cursor()

        data = (home_team, away_team, away_team, ligue_name, game_date, url)

        try:

            cur.execute("INSERT INTO results(home_team, away_team, win_team, ligue_name, date, url) VALUES(?, ?, ?, ?, ?, ?)", data)
            conn.commit()

            cur.close()
            conn.close()
            

        except sqlite3.IntegrityError:

            cur.close()
            conn.close() 

    elif (not preds) & (not other_pred): 
    
        conn = sqlite3.connect('lib/data_results/results_db.db')
        cur = conn.cursor()

        data = (home_team, away_team, "DRAW", ligue_name, game_date, url)

        try:

            cur.execute("INSERT INTO results(home_team, away_team, win_team, ligue_name, date, url) VALUES(?, ?, ?, ?, ?, ?)", data)
            conn.commit()

            cur.close()
            conn.close()
            

        except sqlite3.IntegrityError:

            cur.close()
            conn.close()


def predict(url):

    datas = get_datas(url)

    teams = datas[2]
    home_team = teams[0].replace("-", " ")
    away_team = teams[1].replace("-", " ")
    ligue_name = datas[0].replace(" ", "")
    game_date= datas[1]


    if ligue_name =="Ligue1":
        map_values = {
            "Paris S-G": "Paris Saint Germain",
            "Brest": "Stade Brestois",
            "Lille": "Lille OSC",
            "Nice": "OGC Nice",
            "Lens": "RC Lens",
            "Marseille": "Olympique de Marseille",
            "Lyon": "Olympique Lyonnais",
            "Rennes": "Stade Rennais",
            "Toulouse": "Toulouse FC",
            "Reims": "Stade de Reims",
            "Montpellier": "Montpellier Hérault",
            "Nantes": "FC Nantes",
            "Le Havre": "Le Havre AC",
            "Lorient": "FC Lorient",

        }

    if ligue_name == "LaLiga":

        map_values = {

            "Girona" : "Girona FC",
            "Barcelona" : "FC Barcelone",
            "Betis" : "Betis Séville",
            "Valencia" : "Valence",
            "Getafe" : "Getafe CF",
            "Alavés" : "Deportivo Alavés",
            "Sevilla" : "FC Séville",
            "Osasuna" :  "CA Osasuna",
            "Las Palmas" : "UD Las Palmas",
            "Mallorca" : "Majorque",
            "Cadiz" : "Cadix",
            "Granada" : "Granada CF",
            "Almería" :"UD Almería"

        }

    if ligue_name == "PremierLeague":

        map_values = {


            "Newcastle Utd" : "Newcastle",
            "Newcastle United": "Newcastle",
            "Manchester Utd" : "Manchester United",
            "Brighton" : "Brighton & Hove Albion",
            "Brighton and Hove Albion" : "Brighton & Hove Albion",
            "Wolverhampton Wanderers" : "Wolverhampton",
            "Wolves" : "Wolverhampton",
            "Nott'ham Forest" : "Nottingham Forest",
            "Sheffield Utd" : "Sheffield United",
            "West Ham United" : "West Ham",
            "Tottenham Hotspur"  :"Tottenham"

        }

    if ligue_name == "SerieA":

        map_values = {

            "Inter" : "Inter Milan",
            "Milan" : "AC Milan",
            "Juventus" : "Juventus Turin",
            "Bologna" : "Bologne",
            "Roma" : "AS Roma",
            "Lazio" : "Lazio Rome",
            "Napoli" : "Naples",
            "Internazionale" : "Inter Milan"

        }

    if ligue_name == "Bundesliga":

        map_values = {

            "Bayer Leverkusen" : "BAYER 04 LEVERKUSEN",
            "Leverkusen" : "BAYER 04 LEVERKUSEN",
            "Eint Frankfurt" : "Eintracht Francfort",
            "Freiburg" : "Fribourg",
            "Hoffenheim" : "TSG 1899 Hoffenheim",
            "Augsburg" : "FC Augsburg",
            "Heidenheim" : "FC Heidenheim",
            "Werder Bremen" : "Werder Brême",
            "Monchengladbach" : "Mönchengladbach",
            "M'Gladbach" : "Mönchengladbach",
            "Union Berlin" : "FC Union Berlin",
            "Mainz" : "Mayence",
            "Köln" : "Cologne",
            "Darmstadt" : "SV Darmstadt 98",
            "Mainz 05" : "Mayence"

        }

    mapping = MissingDict(**map_values)

    matches = pd.read_csv("lib/matches_" + ligue_name + ".csv") 
    np_matches = pd.read_csv("lib/np_matches_" + ligue_name + ".csv")

    np_matches["team"]=np_matches["team"].map(mapping)
    np_matches["opponent"]=np_matches["opponent"].map(mapping)

    matches["team"]=matches["team"].map(mapping)
    matches["opponent"]=matches["opponent"].map(mapping)


    matches, new_cols = data_process(matches)

    np_matches = data_process(np_matches)[0]

    preds, other_preds  = make_predictions(matches, np_matches, new_cols,home_team,away_team)

    get_result(preds, other_preds, home_team, away_team, ligue_name, game_date, url)


'''

del matches["comp"]
del matches["round"]
del matches["captain"]
del matches["formation"]
del matches["referee"]

del np_matches["comp"]
del np_matches["round"]
del np_matches["captain"]
del np_matches["formation"]
del np_matches["referee"]

matches["date"] = pd.to_datetime(matches["date"])
matches["target"] = (matches["result"] == "W").astype("int")
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek

np_matches["date"] = pd.to_datetime(np_matches["date"])
np_matches["target"] = (np_matches["result"] == "W").astype("int")
np_matches["venue_code"] = np_matches["venue"].astype("category").cat.codes
np_matches["opp_code"] = np_matches["opponent"].astype("category").cat.codes
np_matches["hour"] = np_matches["time"]
np_matches["day_code"] = np_matches["date"].dt.dayofweek


rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)


train = matches[matches["date"] <'2024-01-01']

test = matches[matches["date"] >'2024-01-01']

predictors = ["venue_code", "opp_code", "hour", "day_code"]


rf.fit(train[predictors], train["target"])

np_matches.hour = np_matches.hour.astype(np.int32)

preds = rf.predict(test[predictors])

error = accuracy_score(test["target"], preds)


combined = pd.DataFrame(dict(actual=test["target"], predicted=preds))

pd.crosstab(index=combined["actual"], columns=combined["predicted"])

precision_score(test["target"], preds)

grouped_matches = matches.groupby("team")


group = grouped_matches.get_group("Paris Saint Germain").sort_values("date")

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]

rolling_averages(group, cols, new_cols)

matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))

matches_rolling = matches_rolling.droplevel('team')

matches_rolling.index = range(matches_rolling.shape[0])

def make_predictions(data, predictors):
    train = data[data["date"] < '2024-01-01']
    test = data[data["date"] > '2024-01-01']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return combined, error


combined, error = make_predictions(matches_rolling, predictors + new_cols)

combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

class MissingDict(dict):
    __missing__ = lambda self, key: key
map_values = {
    "Paris S-G": "Paris Saint Germain"
}
mapping = MissingDict(**map_values)

combined["new_team"] = combined["team"].map(mapping)

merged = combined.merge(combined, left_on=["date", "new_team"], right_on=["date", "opponent"])

merged[(merged["predicted_x"] == 1) & (merged["predicted_y"] ==0)]["actual_x"].value_counts()
'''