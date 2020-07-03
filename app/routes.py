from app import app, db
from app.models import *
import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for, abort
from app.forms import *
from app.utils import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from time import time


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(date, format='medium'):
    if type(date) == str:
        date = dateutil.parser.parse(date)
    if format == 'full':
        format = "yyyy.MM.dd G 'at' HH:mm:ss"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # query all venues
    venues = db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).all()
    # distribute venues to areas where areas -> {("City_1", "State_1"): [list_of_venues], ...}
    areas = {}
    for venue in venues:
        if (venue.city, venue.state) not in areas:
            areas[(venue.city, venue.state)] = []
        areas[(venue.city, venue.state)].append([venue.id, venue.name])

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search/<search_term>', methods=['GET'])
def search_venues(search_term):
    # run a join query on Venues using lazy='joined' mode
    results = db.session.query(Venue).options(joinedload(Venue.shows)).filter(
        Venue.name.ilike(f"%{search_term}%")).all()
    data = []
    for venue in results:
        temp = {"id": venue.id, "name": venue.name, "num_upcoming_shows": venue.shows}
        data.append(temp)
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/search', methods=['POST'])
def search_venues_receiver():
    search_term = request.form.get('search_term', '')
    return redirect(url_for("search_venues", search_term=search_term))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # verify that the given id maps to an existing venue
    venue = db.session.query(Venue).get_or_404(venue_id)
    # split genres string to an array of genres
    venue.genres = venue.genres.split(",")
    venue_shows = db.session.query(Show).options(joinedload(Show.artist, innerjoin=True)).filter(
        Show.venue_id == venue.id).all()
    # classify the venue_shows' into past and upcoming shows based on their start time
    past_shows = []
    upcoming_shows = []
    for show in venue_shows:
        temp = {"artist_id": show.artist_id, "start_time": show.date, "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link}
        upcoming = show.date >= datetime.utcnow()
        if upcoming:
            upcoming_shows.append(temp)
        else:
            past_shows.append(temp)
    # add past and upcoming shows as attributes to the class object venue
    venue.past_shows = past_shows
    venue.upcoming_shows = upcoming_shows
    venue.past_shows_count = len(past_shows)
    venue.upcoming_shows_count = len(upcoming_shows)
    return render_template('pages/show_venue.html', venue=venue)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = VenueForm()
    if not form.validate_on_submit():
        return render_template('forms/new_venue.html', form=form)
    # if form validation is True, add new venue to db
    try:
        # create_instance(Object, form) is a utils function that creates a venue instance of Venue.
        venue = create_instance(Venue, form)
        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash(f'Error, {request.form["name"]} could not be listed.')
        return render_template('forms/new_venue.html', form=form)
    # on successful db insert, flash success
    flash(f'Venue {request.form["name"]} was successfully listed!')
    return redirect(url_for('index'))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  --------------------------------------------------------------------------------------------------------------------
#  Artists
#  --------------------------------------------------------------------------------------------------------------------
@app.route('/artists')
def artists():
    data = db.session.query(Artist.id, Artist.name).order_by(Artist.id).all()
    # TODO: Order the artists based on the number of the shows for each
    # data.sort(key=lambda artist: db.session.query(Show).filter(Show.artist_id == artist.id).count())
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search/<search_term>', methods=['GET'])
def search_artists(search_term):
    """
    search_artists gets any GET request for an artist search
    :param search_term: String
    :return: template -> search_artists.html
    """
    response = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike(f'%{search_term}%')).all()
    return render_template('pages/search_artists.html', results=response, search_term=search_term,
                           num_res=len(response))


@app.route('/artists/search', methods=['POST'])
def search_artists_receiver():
    """
    search_artists_receiver receives any POST request for searching an artist
    :return: redirects to search_artists function
    """
    search_term = request.form.get('search_term', '')
    return redirect(url_for('search_artists', search_term=search_term))


@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    # verify that the given id maps to an existing artist
    artist = db.session.query(Artist).get_or_404(artist_id)

    artist.genres = artist.genres.split(",")
    # getting the artist's shows -> Time Complexity: O(m) where m is the number of shows
    artist_shows = artist.shows
    # classifying shows based on the start_time -> Time Complexity: O(m)
    upcoming_shows = []
    past_shows = []
    for show in artist_shows:
        up_coming = datetime.utcnow() <= show.date
        if up_coming:
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
    artist.upcoming_shows = upcoming_shows
    artist.upcoming_shows_count = len(upcoming_shows)
    artist.past_shows = past_shows
    artist.past_shows_count = len(past_shows)

    return render_template('pages/show_artist.html', artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    form = ArtistForm()
    # verify that the given id maps to an existing artist
    artist = db.session.queery(Artist).get_or_404(artist_id)
    if request.method == 'POST' and form.validate_on_submit():
        error = False
        try:
            # create_instance(Object, form) creates an artist instance of Artist
            artist = update_instance(artist, form)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if not error:
            # on successful db update, flash success
            flash('Artist ' + request.form['name'] + ' was updated successfully!')
            return redirect(url_for('show_artist', artist_id=artist_id))
        # on error db update, flash success
        flash(f'server error occurred, {request.form["name"]} could was not updated')

    data = build_object(artist)
    return render_template('forms/edit_artist.html', form=form, artist=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    error = False
    try:
        # create_instance(Object, form) creates an artist instance of Artist
        artist = create_instance(Artist, form)
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash(f'server error occurred, {request.form["name"]} could not be listed')
        return render_template("forms/new_artist.html", form=form)
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    error = False
    if not form.validate_on_submit():
        return render_template('forms/new_show.html', form=form)
    try:
        show = Show()
        show.artist_id = request.form.get("artist_id")
        show.venue_id = request.form.get("venue_id")
        show.date = request.form.get("start_time")
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
        return render_template('forms/new_show.html', form=form)
    flash('Show was successfully listed!')
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
