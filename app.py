from flask import Flask, render_template, request

from json_handler import *

songs_db = Songdb()

app = Flask(__name__)

@app.route("/base")
def base():
	return render_template("base.html")

@app.route("/")
def index():
	return render_template("index.html",songs_data = songs_db.getData())

@app.route("/addSong", methods=["GET",'POST'])
def addSong():
	data = request.form.to_dict()
	name = data["name"]
	artist = data["artist"]
	print("data: ",data)
	print(f"added song details-\nname: {data['name']}\nartist: {data['artist']}")
	songs_db.addSong(name,artist)
	return render_template("index.html",songs_data = songs_db.getData())


if __name__=="__main__":
	app.run(debug=True)