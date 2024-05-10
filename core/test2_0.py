competitions_url = ["https://fbref.com/en/comps/9/Premier-League-Stats","https://fbref.com/en/comps/20/Bundesliga-Stats","https://fbref.com/en/comps/13/Ligue-1-Stats","https://fbref.com/en/comps/12/La-Liga-Stats","https://fbref.com/en/comps/11/Serie-A-Stats"]

for comp in competitions_url:
    print(comp)

    competition_name = comp.split("/")[-1].replace("-Stats", "").replace("-", " ").replace(" ", "")

    print(competition_name)