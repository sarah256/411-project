from flask import Flask, render_template, request, jsonify, current_app, g
from flask.cli import with_appcontext
import sqlite3
import click
from TwitterClient import TwitterClient
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html") 

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
		sentiment = api.get_sentiment(tweets)

	return render_template("home.html", tweets=sentiment) 

if __name__ == "__main__":
    app.run(debug=True)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

