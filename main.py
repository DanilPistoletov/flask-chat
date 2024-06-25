from flask import Flask, render_template, request, redirect
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def get_messages():
    return render_template('chat.html')

@app.route('/submit', methods=['POST'])
def submit():
    gettime = datetime.now()
    gettime = gettime.strftime("%H:%M")
    msg = request.form['text']
    ava = "\"{{ url_for('static', filename='avatar.png') }}\""
    msg1 = f"""\n<div class="container">
  <img src={ava} alt="Avatar" style="width:30px;">
  <p>{msg}</p>
  <span class="time-right">{gettime}</span>
</div>"""
    file = open(
        "messages.html",
        "r+")
    file.write(msg1)
    return redirect("/")

if __name__ == "__main__":
    app.run()