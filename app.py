from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session

import sqlite3
from datetime import datetime

from lib.predict import predict
import lib.scraping

app = Flask("app")
app.secret_key = "pronobobo"


@app.route('/')
def index():

    return render_template('index.html')

@app.route("/update_data", methods=["POST"])
def update_data():

    try :

        if session["username"] == "admin" :

            lib.scraping.update_data()
            return redirect("/admin")

    except KeyError :

        return redirect("/")


@app.route("/submit_url", methods=["POST"])
def submit_url():

    urlvar = request.form["url"]

    # Vérifier si l'URL est déjà dans la base de données
    conn = sqlite3.connect('lib/data_results/results_db.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM results WHERE url = ?", (urlvar,))
    url_count = cur.fetchone()[0]
    conn.close()

    # Si l'URL est déjà présente, affichez un message d'erreur et redirigez l'utilisateur vers la page de résultats
    if url_count > 0:
        return redirect(url_for("results"))

    # Si l'URL n'est pas déjà présente, appelez la fonction predict
    predict(urlvar)

    return redirect(url_for("results"))


@app.route("/results")
def results():

    conn = sqlite3.connect('lib/data_results/results_db.db')
    cur = conn.cursor()

    # Extrait toutes les lignes de la table "results"
    cur.execute("SELECT home_team, away_team, win_team, ligue_name, date, url FROM results")
    results = cur.fetchall()

    # Formater la date
    formatted_results = []
    for row in results:
        date_obj = datetime.strptime(row[4], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        formatted_results.append((row[0], row[1], row[2], row[3], formatted_date, row[5]))

    headers = ["Home Team", "Away Team", "Winner", "League", "Date", "Link"]

    cur.close()
    conn.close()

    return render_template('results.html', headers=headers, results=formatted_results)


@app.route("/help")
def help():

    return render_template('help.html')

@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST" :

        uservar = request.form["username"] 
        passwdvar = request.form['pwd']
        
        conn = sqlite3.connect('static/assets/db/db.db')
        cur = conn.cursor()

        data = (uservar, passwdvar)

        cur.execute("""SELECT username, password FROM users WHERE username=? AND password=?""", data)

        liste = cur.fetchone()


        if liste !=  None:

            userData = []
            for i in liste :
                userData.append(i)

            session["username"] = userData[0]

            cur.close()
            conn.close()

            return redirect(url_for('index'))
        

        else: 

            cur.close()
            conn.close()

            flash("Wrong username or password. Please retry.")

            return redirect(url_for('login'))
    
    else :

        return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():

    session.pop("username")

    return redirect("/")

@app.route("/admin", methods=["GET", "POST"])
def admin():

    try :

        if session["username"] == "admin" :

            return render_template("admin.html")

    except KeyError :

        return redirect("/")

@app.route("/addAccount", methods=["POST"])
def addAccount():

    uservar = request.form['username'] 
    passwdvar = request.form['pwd']

    conn = sqlite3.connect('static/assets/db/db.db')
    cur = conn.cursor()

    data = (uservar, passwdvar)

    try:

        cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", data)
        conn.commit()

        cur.close()
        conn.close()

        flash("Account registered.")
        return redirect(url_for('admin'))
        

    except sqlite3.IntegrityError:

        cur.close()
        conn.close()

        flash("Username already used.")
        return redirect(url_for('admin'))
    
@app.route("/deleteAccount", methods=["POST"])
def deleteAccount():

    uservar = request.form['username'] 
    passwdvar = request.form['pwd']

    conn = sqlite3.connect('static/assets/db/db.db')
    cur = conn.cursor()

    data = (uservar, passwdvar)

    cur.execute('SELECT * FROM users WHERE username = ? and password = ?', data)
    conn.commit()

    liste = cur.fetchall()

    if len(liste) > 0:



        cur.execute("DELETE FROM users WHERE username=? AND password=?", data)
        conn.commit()

        cur.close()
        conn.close()

        flash("Account deleted.")
        return redirect(url_for('admin'))
        

    else :

        cur.close()
        conn.close()

        flash("An error occurred while deleting the account. Please check data.")

        return redirect(url_for('admin'))


if __name__ == '__main__': 
    print("\n----------------------------------\n")
    print("Pronobo web server running smoothly.\n")
    print("------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)