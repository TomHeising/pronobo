from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session

import sqlite3

app = Flask("app")
app.secret_key = "pronobobo"


@app.route('/')
def index():



    return render_template('index.html')

@app.route("/results")
def results():

    return render_template('results.html')

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

    try:

        cur.execute("DELETE FROM users WHERE username=? AND password=?", data)
        conn.commit()

        cur.close()
        conn.close()

        flash("Account deleted.")
        return redirect(url_for('admin'))
        

    except sqlite3.Error as e:

        cur.close()
        conn.close()

        flash("An error occurred while deleting the account.")
        print("An error occurred:", e)  # Affiche l'erreur dans la console à des fins de débogage
        return redirect(url_for('admin'))


if __name__ == '__main__': 
    print("\n----------------------------------\n")
    print("Pronobo web server running smoothly.\n")
    print("------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)