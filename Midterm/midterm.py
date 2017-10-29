from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

#WTForms will validate that text is entered 
class MovieSearchForm(FlaskForm):
    movie = StringField('Enter the name of your favorite movie:', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/index')
def index():
    simpleForm = MovieSearchForm()
    return render_template('form1.html', form=simpleForm)


@app.route('/movieresult', methods = ['GET', 'POST'])
def result():
	form = MovieSearchForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		movie = form.movie.data
		base_url = "https://itunes.apple.com/search?term="
		url = base_url + movie
		x = requests.get(url, params = {"media": "movie"}).text
		x = json.loads(x)["results"][0]["longDescription"]
		return render_template('movie_data.html', objects = x)
@app.route('/movietext/<moviename>')
def response1(moviename):
	x = make_response("Your favorite movie is " + moviename)
	x.set_cookie("movie", "moviename")
	return x 
@app.route('/tvsearch', methods = ['GET', 'POST'])
def tv_data():
	return render_template('tv-form.html')
@app.route('/tv-search-result', methods = ['POST'])
def tv_search():
	tvshow = request.form['tvshow']
	#print(result['tvshow'])
	base_url = "https://itunes.apple.com/search?term="
	url = base_url + tvshow
	x = requests.get(url, params = {"media": "tvShow"}).text
	x = json.loads(x)["results"]
	#print(x)
	return render_template("tv_template.html", data = x, tvshow = tvshow)
@app.errorhandler(404)
def handle_error404(e404):
	return render_template('404error.html'), 404
@app.errorhandler(405)
def handle_error405(e405):
	return render_template('405error.html'), 405
@app.route('/tv_data/<tvshow>', methods = ['GET', 'POST'])
def get_tv_data(tvshow):
	#print (favorite_mov)
	base_url = "https://itunes.apple.com/search?term=" 
	url = base_url + tvshow
	x = requests.get(url, params = {"entity": "tvEpisode"}).text
	#print(x)
	x = json.loads(x)["results"][0]["previewUrl"]
	y = requests.get(url, params = {"media": "tvShow"}).text
	y = json.loads(y)["results"][0]["longDescription"]
	return render_template('tv_data.html', objects = x, favorite_tv_show=tvshow, y = y, gossipgirl = "Gossip Girl" in tvshow)
	
if __name__ == '__main__':
    app.run()
