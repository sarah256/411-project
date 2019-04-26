from flask import Flask, render_template, request, jsonify
from TwitterClient import TwitterClient
import requests
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html") 

@app.route("/input", methods=["POST"])
def input_text():
	#NOTE - make sure to put API key into url
	url = "https://api.themoviedb.org/3/discover/movie?api_key=XXX&language=en-US&sort_by=popularity.desc&with_genres=28"
	r = requests.get(url)
	full_json = r.json()
	movies = {} # key: movie name ; value: sentiment
	movie_images = {}
	# print(full_json)
	for movie in full_json['results']:
		movies[movie['title']] = []
		movie_images[movie['title']] = movie['poster_path']

	if request.method == "POST":
		print(request.form)
		data = request.form['submitText']
		print(data)
		query = data
		# creating object of TwitterClient Class 
		api = TwitterClient() 
		# calling function to get tweets
		count = 0
		final_movies = {}
		for movie in movies: 
			tweets = api.get_tweets(query = movie, count = 100)
			sentiment = api.get_sentiment(tweets)
			final_movies[movie] = sentiment[0]
			count = count + 1
			if count == 5:
				break
		print(final_movies)

	return render_template("home.html", movies=final_movies, images=movie_images) 

if __name__ == "__main__":
    app.run(debug=True)