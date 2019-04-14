import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main(album_or_tracks):
    if album_or_tracks == "album":
        mgmt = Album(name="Oracular Spectacular", artist="MGMT", num_tracks=10)
        db.session.add(mgmt)
        db.session.commit()

    elif album_or_tracks == "tracks":
        album = Album.query.get(1)

        album.add_track(title="Time to Pretend", duration=261, number=1, side=1, start=0, end=1)
        album.add_track(title="Weekend Wars", duration=252, number=2, side=1, start=1, end=2)
        album.add_track(title="The Youth", duration=228, number=3, side=1, start=2, end=3)
        album.add_track(title="Electric Feel", duration=230, number=4, side=1, start=3, end=4)
        album.add_track(title="Kids", duration=303, number=5, side=1, start=4, end=5)
        album.add_track(title="4th Dimensional Transition", duration=238, number=6, side=2, start=5, end=6)
        album.add_track(title="Pieces of What", duration=164, number=7, side=2, start=6, end=7)
        album.add_track(title="Of Moons, Birds & Monsters", duration=287, number=8, side=2, start=7, end=8)
        album.add_track(title="The Handshake", duration=220, number=9, side=2, start=8, end=9)
        album.add_track(title="Future Reflections", duration=240, number=10, side=2, start=9, end=10)

    else:
        "Incorrect input."
if __name__ == "__main__":
    with app.app_context():
        album_or_tracks = input("Add album or tracks?")
        main(album_or_tracks)