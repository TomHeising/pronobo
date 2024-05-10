import pandas as pd
import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model

competitions_url = ["https://fbref.com/en/comps/9/Premier-League-Stats","https://fbref.com/en/comps/20/Bundesliga-Stats","https://fbref.com/en/comps/13/Ligue-1-Stats","https://fbref.com/en/comps/12/La-Liga-Stats","https://fbref.com/en/comps/11/Serie-A-Stats"]


def calculer_moyenne(matches):
    moyenne = matches.mean()
    return moyenne

for comp in competitions_url:
    
    competition_name = comp.split("/")[-1].replace("-Stats", "").replace("-", " ").replace(" ", "")

    df = pd.read_csv("matches_" + competition_name + ".csv", index_col=0)
    df_2 = pd.read_csv("np_matches_" + competition_name + ".csv", index_col=0)
    
    for index, row in df_2.iterrows():
    
        opponent = row["opponent"]  
        team = row["team"]
        
        matches = df[(df['team'] == team) & (df['opponent'] == opponent)]
            
        moyenne_attributs = calculer_moyenne(matches[['gf', 'ga', 'xg', 'xga', 'poss', 'sh', 'sot', 'dist', 'fk', 'pk','pkatt','attendance']])
    
        df_2.at[index, 'gf'] = moyenne_attributs['gf']
        df_2.at[index, 'ga'] = moyenne_attributs['ga']
        df_2.at[index, 'xg'] = moyenne_attributs['xg']
        df_2.at[index, 'xga'] = moyenne_attributs['xga']
        df_2.at[index, 'poss'] = moyenne_attributs['poss']
        df_2.at[index, 'sh'] = moyenne_attributs['sh']
        df_2.at[index, 'sot'] = moyenne_attributs['sot']
        df_2.at[index, 'dist'] = moyenne_attributs['dist']
        df_2.at[index, 'fk'] = moyenne_attributs['fk']
        df_2.at[index, 'pk'] = moyenne_attributs['pk']
        df_2.at[index, 'pkatt'] = moyenne_attributs['pkatt']
        df_2.at[index, 'attendance'] = moyenne_attributs['attendance']

    df_2.to_csv("np_matches_" + competition_name + ".csv")

