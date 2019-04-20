import os

import requests
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

play_status = "paused"
current_track = 0

def get_play_status():
    return play_status

def set_play_status(my_status):
    return my_status

def get_current_track():
    return current_track

def set_current_track(my_track):
    return my_track

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/albums")
def albums():
    albums = Album.query.all()
    return render_template("albums.html", albums=albums)

@app.route("/albums/<string:album_id>")
def album(album_id):
    album = Album.query.filter_by(id=album_id).first()
    tracks = Track.query.filter_by(album_id=album_id).order_by(Track.number).all()
    return render_template("album.html", album=album, tracks=tracks)

@app.route("/play/albums/<string:album_id>/<string:track_id>", methods=['GET','POST'])
def play(album_id, track_id):
    album = Album.query.filter_by(id=album_id).first()
    tracks = Track.query.filter_by(album_id=album_id).order_by(Track.number).all()
    track = Track.query.get(track_id)
    if request.method == 'POST':
        current_track = track_id
        if 'play' in request.form:
            set_play_status("play")
        elif 'pause' in request.form:
            set_play_status("paused")
        elif 'next' in request.form:
            set_current_track(int(track_id) + 1)
            set_play_status("play")
        elif 'previous' in request.form:
            set_current_track(int(track_id) - 1)
            set_play_status("play")
        
    return render_template("play.html", album=album, tracks=tracks, track=track)

@app.route("/api/albums/<string:album_id>")
def getAlbumData(album_id):
    album = Album.query.filter_by(id=album_id).first()
    tracks = Track.query.filter_by(album_id=album_id).order_by(Track.number).all()
    track_num_and_title = {}
    for track in tracks:
        track_num_and_title[track.title] = track.number

    return jsonify({
        "album_title": album.name,
        "album_artist": album.artist,
        "num_tracks": album.num_tracks,
        "tracks": track_num_and_title,
        })

@app.route("/api/albums/<string:album_id>/<string:track_id>", methods=['GET'])
def getTrackData(album_id, track_id):
    track = Track.query.filter_by(id=track_id).first()

    return jsonify({
        "track_title": track.title,
        "duration": track.duration,
        "number": track.number,
        "side": track.side,
        "start": track.start,
        "end": track.end,
        })

@app.route("/api/albums/<string:album_id>/<string:track_id>/set", methods=['PUT'])
def setTrackData(album_id, track_id):
    track = Track.query.get(track_id)
    data = request.get_json() or {}
    return jsonify(data)
    #track.start = data[]

@app.route("/api/play_status")
def play_status_route():
    return jsonify({
        "play_status": get_play_status()
        })

@app.route("/api/current_track")
def current_track():
    track = Track.query.get(current_track)
    return jsonify({
        "track_title": track.title,
        "duration": track.duration,
        "number": track.number,
        "side": track.side,
        "start": track.start,
        "end": track.end,
        })

@app.route("/api/play", methods=['POST'])
def playing():
    if methods == 'POST':
        playing = request.form.get("Play")
        return "Now playing."
        
    elif methods == 'GET':
        return jsonify({
            "playing": playing
            })
