## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests, json
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album name?', validators=[Required()])
    rating = RadioField('How much do you like this album? (1 low, 3 high)', choices =[(1, '1'), (2, "2"), (3, "3")], validators=[Required()])
    submit = SubmitField('Submit')



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

#New Routes

@app.route('/artistform')
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artistinfo():
    if request.method == "GET":
        artist = request.args.get("artist", "")
        url = "https://itunes.apple.com/search?term=" + artist
        result = requests.get(url)
        objects = result.json()["results"]
        return render_template("artist_info.html", objects=objects)
    else:
        return "Please enter a valid artist name!"

@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def artist_name(artist_name):
    url = "https://itunes.apple.com/search?term=" + artist_name
    result = requests.get(url)
    results = result.json()["results"]
    return render_template("specific_artist.html", results=results)

@app.route('/album_entry')
def album_entry():
    albumForm = AlbumEntryForm()
    return render_template("album_entry.html", form=albumForm)

@app.route('/album_result', methods=['GET', 'POST'])
def album_result():
    if request.method == "POST":
        album_name = request.form["album"]
        rating = request.form["rating"]
        return render_template('album_data.html', rating=rating, album_name=album_name)
    else:
        return "Error!"




if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
