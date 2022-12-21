from flask import Flask, render_template
import sqlite3
import os
db = os.path.dirname(os.path.abspath(__file__)) + "/robofest.db"
result=''
def readTable():
    sqlite_connection = sqlite3.connect(db)
    cursor = sqlite_connection.cursor()
    cursor.execute("select * from users")
    result=cursor.fetchall()
    print (result)
    cursor.close()
    return result

readTable()
app = Flask(__name__)

name='Имя'
@app.route("/")
def home():
    data=readTable()
    return render_template('index.html')

@app.route("/users")
def user():
    data=readTable()
    counter=len(data)
    return render_template('users.html',data=data, counter=counter)


@app.route("/teams")
def team():
    data=readTable()
    counter=len(data)
    return render_template('teams.html',data=data, counter=counter)

@app.route("/naminations")
def namination():
    data=readTable()
    counter=len(data)
    return render_template('naminations.html',data=data, counter=counter)

@app.route("/allinfo")
def allinfo():
    data=readTable()
    counter=len(data)
    return render_template('allinfo.html',data=data, counter=counter)

@app.route("/about")
def about():
    data=readTable()
    counter=len(data)
    return render_template('about.html',data=data, counter=counter)

if __name__=="__main__":
    app.run(debug=True)



