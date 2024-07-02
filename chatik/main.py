from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
app = Flask(__name__)

con = sqlite3.connect('messages.db', check_same_thread=False)
cursor = con.cursor()

@app.route("/")
def get_messages():
    app.jinja_env.cache = {}
    cursor.execute("SELECT MAX(ID) FROM messages;")
    id = int(cursor.fetchone()[0]) + 1
    id0 = 1
    with open(
            "messages.html",
            'w', encoding='utf8') as f:
        f.write("")
    while id0 != id:
        ava = "\"{{ url_for('static', filename='avatar.png') }}\""
        cursor.execute(f"SELECT text FROM messages WHERE ID = {id0};")
        text = cursor.fetchone()[0]
        cursor.execute(f"SELECT time FROM messages WHERE ID = {id0};")
        time = cursor.fetchone()[0]
        msg = f"""\n<div class="container">
          <img src={ava} alt="Avatar" style="width:30px;">
          <p>{text}</p>
          <span class="time-right">{time}</span>
        </div>"""
        with open("messages.html", 'a', encoding='utf8') as f:
            f.write(msg)
        id0 += 1
    return render_template('chat.html')

@app.route('/submit', methods=['POST'])
def submit():
    cursor.execute("SELECT MAX(ID) FROM messages;")
    id = int(cursor.fetchone()[0]) + 1
    gettime = datetime.now()
    gettime = gettime.strftime("%H:%M")
    msg = request.form['text']
    cursor.execute(f"INSERT INTO messages(id, text, time) VALUES('{id}', '{msg}', '{gettime}');")
    con.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()