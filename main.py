from TwitterClient import TwitterClient
import requests
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth


app = Flask(__name__)

app = Flask(__name__)
app.config['GOOGLE_ID'] = ""
app.config['GOOGLE_SECRET'] = ""
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return render_template("home.html") 


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
 

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
