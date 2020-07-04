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


# home page

@app.route('/')
def index():
    return render_template('pages/home.html')


#  --------------------------------------------------------------------------------------------------------------------
#  Venues
#  --------------------------------------------------------------------------------------------------------------------

@app.route('/venues/')
def venues():
    # query all venues, order by venue id.
    venues = db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).order_by(Venue.id).all()

    # distribute venues to areas where areas -> {("City_1", "State_1"): [list_of_venues], ...}.
    areas = {}
    for venue in venues:
        if (venue.city, venue.state) not in areas:
            areas[(venue.city, venue.state)] = []
        areas[(venue.city, venue.state)].append([venue.id, venue.name])

    return render_template('pages/venues.html', areas=areas)


#  Create Venue

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()

    # if form is not valid, flash error.
    if not form.validate_on_submit():
        flash(f'Please insert valid data!')
        return render_template('forms/new_venue.html', form=form)

    error = False
    try:
        venue = Venue()
        # get attributes of venue instance.
        attributes = dir(venue)
        # Update the values of the venue attributes with the given values ->
        # update_instance(venue_instance, form_instance, [attributes]).
        venue = update_instance(venue, form, attributes)
        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        # on failure db insert, flash error.
        flash(f'Error, {request.form["name"]} could not be listed.')
        return render_template('forms/new_venue.html', form=form)
    # on successful db insert, flash success
    flash(f'Venue {request.form["name"]} was successfully listed!')
    return redirect(url_for('index'))


# search venue

@app.route('/venues/search/<search_term>', methods=['GET'])
def search_venues(search_term):
    # join venues and shows and search form a given term
    results = db.session.query(Venue).options(joinedload(Venue.shows)).filter(
        Venue.name.ilike(f"%{search_term}%")).all()

    data = []
    for venue in results:
        temp = {"id": venue.id, "name": venue.name, "num_upcoming_shows": venue.shows}
        data.append(temp)

    # form response object
    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/search', methods=['POST'])
def search_venues_receiver():
    """
    search_venues_receiver receives a POST request for searching an venue with with a given search_term
    :return: redirects to search_venues function
    """
    search_term = request.form.get('search_term', '')
    return redirect(url_for("search_venues", search_term=search_term))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # verify that the given id maps to an existing venue.
    venue = db.session.query(Venue).get_or_404(venue_id)

    # split genres string to an array of genres.
    venue.genres = venue.genres.split(",")

    # join shows and artists to get all shows of the given venue.
    venue_shows = db.session.query(Show).options(joinedload(Show.artist, innerjoin=True)).filter(
        Show.venue_id == venue.id).all()

    # classify the venue_shows' into past and upcoming shows based on their start time.
    past_shows = []
    upcoming_shows = []
    for show in venue_shows:
        temp = {"artist_id": show.artist_id, "start_time": show.start_time, "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link}
        upcoming = show.start_time >= datetime.utcnow()
        if upcoming:
            upcoming_shows.append(temp)
        else:
            past_shows.append(temp)

    # add past and upcoming shows as attributes of the instance variable, venue.
    venue.past_shows = past_shows
    venue.upcoming_shows = upcoming_shows
    venue.past_shows_count = len(past_shows)
    venue.upcoming_shows_count = len(upcoming_shows)

    return render_template('pages/show_venue.html', venue=venue)


# edit venue

@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = db.session.query(Venue).get_or_404(venue_id)
    form = VenueForm()

    # validate a form on submission.
    if request.method == 'POST' and form.validate_on_submit():
        error = False
        try:
            # get attributes of venue instance.
            attributes = dir(venue)
            # update values of venue attributes using utils function -> update_instance(instance_var, form_instance,
            # [attributes]).
            venue = update_instance(venue, form, attributes)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if not error:
            # on successful db update, flash success.
            flash('Venue ' + request.form['name'] + ' was updated successfully!')
            return redirect(url_for('show_venue', venue_id=venue_id))
        # on error db update, flash failed.
        flash(f'server error occurred, {request.form["name"]} could was not updated')

    # populate venue form with the existing venue data using utils function ->
    # set_form_data(form_instance, venue_object).
    form = set_form_data(form, venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<venue_id>/delete', methods=['DELETE', 'GET'])
def delete_venue(venue_id):
    # verify a given id.
    venue = db.session.query(Venue).get_or_404(venue_id)
    venue_name = venue.name

    error = False
    try:
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash(f"Error occurred. {venue_name} was not deleted.")
        return redirect(url_for("show_venue", venue_id=venue_id))
    else:
        flash(f"{venue_name} was deleted successfully.")
        return redirect(url_for("index"))


#  --------------------------------------------------------------------------------------------------------------------
#  Artists
#  --------------------------------------------------------------------------------------------------------------------
@app.route('/artists/')
def artists():
    # Query all artists ordered by their id.
    artists = db.session.query(Artist.id, Artist.name).order_by(Artist.id).all()
    # TODO: Order the artists based on the number of the shows for each
    # data.sort(key=lambda artist: db.session.query(Show).filter(Show.artist_id == artist.id).count())
    return render_template('pages/artists.html', artists=artists)


# create artist

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if not form.validate_on_submit():
        flash(f'Please insert valid data!')
        return render_template("forms/new_artist.html", form=form)

    error = False
    try:
        artist = Artist()
        # get attributes of the artist instance.
        attributes = dir(artist)
        # Update the values of the artist's attributes with the given values from the form ->
        # update_instance(instance_var, form_instance, [attributes]).
        artist = update_instance(artist, form, attributes)
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        # on failure db insert, flash error occurred
        flash(f'server error occurred, {request.form["name"]} could not be listed')
        return render_template("forms/new_artist.html", form=form)
    else:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return redirect(url_for('index'))


# search artist

@app.route('/artists/search/<search_term>', methods=['GET'])
def search_artists(search_term):
    response = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike(f'%{search_term}%')).all()
    return render_template('pages/search_artists.html', results=response, search_term=search_term,
                           num_res=len(response))


@app.route('/artists/search', methods=['POST'])
def search_artists_receiver():
    """
    search_artists_receiver receives a POST request for searching an artist
    :return: redirects to search_artists function
    """
    search_term = request.form.get('search_term', '')
    return redirect(url_for('search_artists', search_term=search_term))


@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    # Verify that the given id maps to an existing artist.
    artist = db.session.query(Artist).get_or_404(artist_id)

    # Transfer genres string to a list.
    artist.genres = artist.genres.split(",")

    # Get all artist's shwos.
    artist_shows = artist.shows

    # Classifying shows based on the start_time.
    upcoming_shows = []
    past_shows = []
    for show in artist_shows:
        up_coming = datetime.utcnow() <= show.start_time
        if up_coming:
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
    artist.upcoming_shows = upcoming_shows
    artist.upcoming_shows_count = len(upcoming_shows)
    artist.past_shows = past_shows
    artist.past_shows_count = len(past_shows)

    return render_template('pages/show_artist.html', artist=artist)


#  Update artist
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    # Verify that the given id maps to an existing artist.
    artist = db.session.query(Artist).get_or_404(artist_id)
    form = ArtistForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = False
        try:
            # get attributes of artist instance.
            attributes = dir(artist)
            # update values of artist attributes using utils function -> update_instance(instance_var, form_instance,
            # [attributes]).
            artist = update_instance(artist, form, attributes)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        if not error:
            # on successful db update, flash success.
            flash('Artist ' + request.form['name'] + ' was updated successfully!')
            return redirect(url_for('show_artist', artist_id=artist_id))
        # on error db update, flash failed.
        flash(f'server error occurred, {request.form["name"]} could was not updated')

    # populate form attributes' data with artist data
    form = set_form_data(form, artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


#  --------------------------------------------------------------------------------------------------------------------
#  Shows
#  --------------------------------------------------------------------------------------------------------------------

@app.route('/shows')
def shows():
    # query all upcoming shows using inner join with both Venue and Show
    upcoming_shows = db.session.query(Show).options(joinedload(Show.artist, innerjoin=True),
                                                    joinedload(Show.venue, innerjoin=True)).filter(
        Show.start_time >= datetime.utcnow()).order_by(Show.start_time).all()

    data = []
    for show in upcoming_shows:
        temp = {"venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time}
        data.append(temp)

    return render_template('pages/shows.html', shows=data)


# create show

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm()
    if not form.validate_on_submit():
        return render_template('forms/new_show.html', form=form)

    error = False
    try:
        show = Show()
        # get all attributes of the show instance.
        attributes = dir(show)
        print(attributes)
        # update the values of the show's attributes with the given values from the form ->
        # update_instance(instance_var, form_instance, [attributes]).
        show = update_instance(show, form, attributes)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        # on failure, flash error message.
        flash('An error occurred. Show could not be listed.')
        return render_template('forms/new_show.html', form=form)
    else:
        # on success, flask success message and rredirect to home page.
        flash('Show was successfully listed!')
        return redirect(url_for("index"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
