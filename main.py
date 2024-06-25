from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('chat.html')

@app.route('/submit', methods=['POST'])
def submit():
    msg = request.form['text']
    msg1 = f"""\n<div class="container">
  <img src="{{ url_for('static', filename='avatar.png') }}" alt="Avatar" style="width:30px;">
  <p>{msg}</p>
  <span class="time-right">11:00</span>
</div>"""
    file = open(
        "messages.html",
        "r+")
    file.write(msg1)
    return file

if __name__ == "__main__":
    app.run()