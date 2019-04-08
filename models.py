from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    num_tracks = db.Column(db.Integer, nullable=False)

    def add_track(self, title, duration, number, start, end):
        t = Track(title=title, album_id=self.id, duration=duration, number=number, start=start, end=end)
        db.session.add(t)
        db.session.commit()


class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Integer, nullable=False)
    end = db.Column(db.Integer, nullable=False)

