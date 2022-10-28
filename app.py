from flask import Flask, render_template,request

from poem import start_task,Output

app = Flask(__name__)

@app.route("/")
def hello_world():
	return render_template("index.html")

@app.route("/api/first_letter_all_match",methods=["POST"])
def first_letter_all_match():
	if request.form["dataset"] == "random":
		tangshi = bool(request.form["tangshi"])
		songci = bool(request.form["songci"])
		songshi = bool(request.form["songshi"])
		num = int(request.form["num"])
		#print(tangshi,songci,songshi,num)
		args = [tangshi,songshi,songci,num]
	elif request.form["dataset"] == "read_all":
		tangshi = bool(request.form["tangshi"])
		songci = bool(request.form["songci"])
		songshi = bool(request.form["songshi"])
		args = [tangshi,songshi,songci]
	elif request.form["dataset"] == "brief":
		args = []

	return Output(start_task("first_letter_all_match",[request.form["letters"]],request.form["dataset"],args)).get_web_string()