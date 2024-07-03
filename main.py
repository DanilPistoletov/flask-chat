from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import sqlite3
from flask_session import Session

version = "1.5"

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
        cursor.execute(f"SELECT username FROM messages WHERE ID = {id0};")
        username = cursor.fetchone()[0]
        msg = f"""\n<div class="container">
          <img src={ava} alt="Avatar" style="width:50px;"><span class="time-right">{time}</span><h4>Ник: {username}</h4><hr>
          <p>{text}</p>
        </div>"""
        with open("messages.html", 'a', encoding='utf8') as f:
            f.write(msg)
        id0 += 1
    return render_template('chat.html')

@app.route('/sms', methods=['POST'])
def sms():
    msg = request.form['text']
    if len(msg) < 1 or len(msg) > 500:
        return "Сообщение не должно быть пустым или более 500 символов"
    elif 0 < len(msg) < 501:
        cursor.execute("SELECT MAX(ID) FROM messages;")
        id = int(cursor.fetchone()[0]) + 1
        gettime = datetime.now()
        gettime = gettime.strftime("%H:%M")
        try:
            if session["name"] is None:
                username = "Анон"
        except:
            username = "Анон"
        else:
            if session["name"] is None:
                username = "Анон"
            else:
                username = session["name"]
        if "<" in msg or ">" in msg or "\"" in msg or "\'" in msg:
            msg = msg.replace("<", "&lt;")
            msg = msg.replace(">", "&gt;")
            msg = msg.replace("\"", "&quot;")
            msg = msg.replace("\'", "&apos;")
        cursor.execute(f"INSERT INTO messages(id, text, time, username) VALUES('{id}', '{msg}', '{gettime}', '{username}');")
        con.commit()
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    login = request.form['reg-login']
    password = request.form['reg-password']
    try:
        cursor.execute(f"SELECT login FROM users WHERE login = '{login}';")
        logincheck = cursor.fetchone()[0]
    except:
        if len(login) < 4 or len(login) > 50:
            return "В логине должно быть не менее 3 и не более 50 символов"
        elif len(login) > 3 and len(login) < 51:
            if len(password) < 10 or len(password) > 200:
                return "Пароль должен состоять из 10 и более символов, но меньше 100 символов"
            elif 9 < len(password) < 201:
                import hashlib
                password = hashlib.sha512(password.encode(encoding='UTF-8'))
                password = password.hexdigest()
                cursor.execute(f"INSERT INTO users(login, password) VALUES('{login}', '{password}');")
                con.commit()
                if request.method == "POST":
                    session["name"] = request.form.get("reg-login")
                    return redirect("/")
    else:
        return "Пользователь уже зарегистрирован"
    return redirect("/")

@app.route("/login", methods=["POST", "GET"])
def login():
    login = request.form['login']
    trypassword = request.form['password']
    try:
        cursor.execute(f"SELECT login FROM users WHERE login = '{login}';")
        logincheck = cursor.fetchone()[0]
    except:
        return "Пользователь не существует"
    else:
        import hashlib
        cursor.execute(f"SELECT password FROM users WHERE login = '{login}';")
        password = cursor.fetchone()[0]
        trypassword = hashlib.sha512(trypassword.encode(encoding='UTF-8'))
        trypassword = trypassword.hexdigest()
        if password == trypassword:
            if request.method == "POST":
                session["name"] = login
                return redirect("/")
        elif password != trypassword:
            return "Пароль не подходит"
    return redirect("/")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/checkupdate", methods=["POST", "GET"])
def checkupdate():
    if session["name"]=="admin":
        import wget
        import os
        wget.download("https://raw.githubusercontent.com/DanilPistoletov/flask-chat/main/main.py", "git.html")
        with open('git.html') as f:
            s = f.read()
            f.close()
            os.remove("git.html")
            if f"version = \"{version}\"" in s:
                return "Версия чата актуальна"
            else:
                return "Чат устарел, загрузите новую версию по адресу github.com/DanilPistoletov/flask-chat/"
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run()