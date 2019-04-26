from flask import Flask, render_template, request, jsonify
from TwitterClient import TwitterClient
import requests
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html") 

@app.route("/input", methods=["POST"])
def input_text():
	genres = {"Action":28,
				"Adventure":12,
				"Animation":16,
				"Comedy":35,
				"Crime":80,
				"Documentary":99,
				"Drama":18,
				"Family":10751,
				"Fantasy":14,
				"History":36,
				"Horror":27,
				"Music":10402,
				"Mystery":9648,
				"Romance":10749,
				"Science Fiction":878,
				"TV Movie":10770,
				"Thriller":53,
				"War":10752,
				"Western":37
				}
	if request.method == "POST":
		print(request.form)
		data = request.form['submitText']
		print(data)
		query = data
		genre_id = genres[query]
		#NOTE - make sure to put API key into url
		url = "https://api.themoviedb.org/3/discover/movie?api_key=XXX&language=en-US&sort_by=popularity.desc&with_genres="+str(genre_id)
		print(url)
		print(query + " this is the query ---------------")
		print(genre_id)
		r = requests.get(url)
		full_json = r.json()
		movies = {} # key: movie name ; value: sentiment
		movie_images = {}
		# print(full_json)
		for movie in full_json['results']:
			movies[movie['title']] = []
			movie_images[movie['title']] = movie['poster_path']
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