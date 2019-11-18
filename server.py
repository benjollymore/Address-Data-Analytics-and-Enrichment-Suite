from flask import request, Flask, render_template
import subprocess

app = Flask(__name__)
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/echo", methods=['POST'])
def echo():
	command = request.form['text']
	print("command from webserver: ",command)
	subprocess.call(command)
	return index()

app.run(debug=True)