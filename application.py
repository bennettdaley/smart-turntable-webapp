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

@app.route("/select_album", methods=['GET'])
def select_album():
    albums = Album.query.all()
    return render_template("select_album.html", albums=albums)

@app.route("/select_track", methods=['POST'])
def select_track():
    #if requst.method == 'GET':
        #playing_album = NowPlaying.query.get(0)
        #album = Album.query.get()
    if request.method == 'POST':
        selection = request.form.get("album_select")
        album = Album.query.get(selection)
        tracks = Track.query.filter_by(album_id=str(album.id)).order_by(Track.number).all()
    return render_template("select_track.html", album=album, tracks=tracks)

@app.route("/play_track", methods=['POST'])
def play_track():
    playing = NowPlaying.query.get(0)
    if 'track_select' in request.form:
        selection = request.form.get("track_select")
        track = Track.query.get(selection)
        album = Album.query.get(track.album_id)
        playing.track_id = track.id
    else:
        if 'play' in request.form:
            playing.is_playing = "playing"
        elif 'pause' in request.form:
            playing.is_playing = "paused"
        elif 'next' in request.form:
            playing.track_id += 1
            playing.is_playing = "playing"
        elif 'previous' in request.form:
            playing.track_id -= 1
            playing.is_playing = "playing"
    db.session.commit()
    track = Track.query.get(playing.track_id)
    album = Album.query.get(track.album_id)
    tracks = Track.query.filter_by(album_id=str(album.id)).order_by(Track.number).all()
    return render_template("play_track.html", album=album, tracks=tracks, track=track, playing=playing.track_id)

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
    playing = NowPlaying.query.get(0)
    return jsonify({
        "play_status": playing.is_playing,
        "current_track": playing.track_id,
        })

@app.route("/api/current_track")
def current_track():
    playing = NowPlaying.query.get(0)
    track = Track.query.get(playing.track_id)
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
