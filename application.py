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
            this_track = Track.query.get(playing.track_id)
            this_album = Album.query.get(this_track.album_id)
            valid_tracks = Track.query.filter_by(album_id=this_album.id).all()
            valid_track_ids = []
            for valid_track in valid_tracks:
                valid_track_ids.append(valid_track.id)
            print(valid_track_ids)
            print(playing.track_id)
            if (playing.track_id + 1) in valid_track_ids:
                playing.track_id += 1
                playing.is_playing = "paused"
        elif 'previous' in request.form:
            this_track = Track.query.get(playing.track_id)
            this_album = Album.query.get(this_track.album_id)
            valid_tracks = Track.query.filter_by(album_id=this_album.id).all()
            valid_track_ids = []
            for valid_track in valid_tracks:
                valid_track_ids.append(valid_track.id)
            print(valid_track_ids)
            print(playing.track_id)
            if (playing.track_id - 1) in valid_track_ids:
                playing.track_id -= 1
                playing.is_playing = "paused"
    db.session.commit()
    track = Track.query.get(playing.track_id)
    album = Album.query.get(track.album_id)
    tracks = Track.query.filter_by(album_id=str(album.id)).order_by(Track.number).all()
    return render_template("play_track.html", album=album, tracks=tracks, track=track, playing=playing.track_id)

@app.route("/add_album")
def addAlbum():
    return render_template("add_album.html")

@app.route("/add_album/add_tracks", methods=['POST'])
def addTracks():
    name = request.form.get("name")
    artist = request.form.get("artist")
    num_tracks = request.form.get("num_tracks")
    album = Album(name=name, artist=artist, num_tracks=int(num_tracks))
    db.session.add(album)
    db.session.commit()
    return render_template("add_tracks.html", album_id=album.id, name=name, artist=artist, num_tracks=int(num_tracks))

@app.route("/add_album/add_tracks/finished", methods=['POST'])
def finishAddingTracks():
    track_titles = request.form.getlist("title")
    album_id = request.form.get("album_id")
    album = Album.query.get(album_id)
    track_num = 1
    for title in track_titles:
        album.add_track(title=title, duration=1, number=track_num, side=1, start=0, end=1)
        track_num += 1
    return render_template("index.html")

@app.route("/select_album_add_track_locations")
def select_album_add_track_locations():
    albums = Album.query.all()
    return render_template("select_album_add_track_locations.html", albums=albums)

@app.route("/add_track_locations", methods=['POST'])
def add_track_locations():
    album_id = request.form.get("album_select")
    tracks = Track.query.filter_by(album_id=album_id).order_by(Track.number).all()
    playing = NowPlaying.query.get(0)
    track_ids = []
    for track in tracks:
        track_ids.append(track.id)
    playing.scan_track_ids = track_ids
    playing.is_playing = "scanning"
    db.session.commit()
    return render_template("index.html")

@app.route("/api/albums/<string:album_id>")
def getAlbumData(album_id):
    album = Album.query.filter_by(id=album_id).first()
    tracks = Track.query.filter_by(album_id=album_id).order_by(Track.number).all()
    track_num_and_title = {}
    track_ids = []
    for track in tracks:
        track_num_and_title[track.title] = track.number
        track_ids.append(track.id)
    return jsonify({
        "album_title": album.name,
        "album_artist": album.artist,
        "num_tracks": album.num_tracks,
        "tracks": track_num_and_title,
        "track_ids": track_ids,
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

@app.route("/api/set_track_location", methods=['POST'])
def set_track_location():
    content = request.get_json() or {}
    track = Track.query.get(content["track_id"])
    track.start = content["start"]
    track.end = content["end"]
    db.session.commit()

@app.route("/api/play_status")
def play_status_route():
    playing = NowPlaying.query.get(0)
    return jsonify({
        "play_status": playing.is_playing,
        "current_track": playing.track_id,
        "scan_track_ids": playing.scan_track_ids
        })

@app.route("/api/set_play_status", methods=['POST'])
def set_play_status_route():
    content = request.get_json() or {}
    playing = NowPlaying.query.get(0)
    playing.is_playing = content["is_playing"]
    playing.scan_track_ids = content["set_track_data"]
    db.session.commit()

@app.route("/api/current_track")
def current_track():
    playing = NowPlaying.query.get(0)
    track = Track.query.get(playing.track_id)
    return jsonify({
        "id": track.id,
        "track_title": track.title,
        "duration": track.duration,
        "number": track.number,
        "side": track.side,
        "start": track.start,
        "end": track.end,
        })