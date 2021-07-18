from flask import Flask, render_template

from json_handler import *

songs_db = Songdb()

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html",songs_data = songs_db.getData())