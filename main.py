from flask import Flask, render_template, request, jsonify
from TwitterClient import TwitterClient
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("api_prototype.html") 

@app.route("/input", methods=["POST"])
def input_text():

	if request.method == "POST":
		print(request.form)
		data = request.form['submitText']
		print(data)
		query = data
		# creating object of TwitterClient Class 
		api = TwitterClient() 
		# calling function to get tweets 
		tweets = api.get_tweets(query = query, count = 100)

	return render_template("api_prototype.html", tweets=tweets) 

if __name__ == "__main__":
    app.run(debug=True)