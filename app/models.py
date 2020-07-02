from app import db


# Models.

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    # create a relationship between Venue and Show. To get the venue of a show run (show_obj.venue).
    # To get all shows of a venue (venue_obj.shows)
    venue = db.relationship("Venue", backref=db.backref("shows", lazy='select', cascade="all, delete-orphan"))
    # create a relationship between Artist and Show. To get the artist of a show_ run (show_obj.artist).
    # To get all shows for an artist (artist_obj.shows)
    artist = db.relationship("Artist", backref=db.backref("shows", lazy='select', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"Show <{self.id}, {self.venue_id}, {self.artist_id}, {self.date}>"


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120))
    # create a relationship between venues and artists. To get artists that performed in a venue run (
    # venue_obj.artists). To get all venues which an artist performed in run (artist_obj.venues)
    artists = db.relationship('Artist', secondary='shows', backref=db.backref("venues", lazy="select"))

    def __repr__(self):
        return f"Venue <{self.id}, {self.name}, {self.city}, {self.state}, {self.address}, {self.phone}, " \
               f"{self.image_link}, {self.facebook_link}>"


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
        return f"Artist <{self.id}, {self.name}, {self.city}, {self.state}, {self.phone}, {self.genres} " \
               f"{self.image_link}, {self.facebook_link}>"
