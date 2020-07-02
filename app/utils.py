from flask import request, abort
from app import db


def create_instance(model, form):
    new_ins = model()
    new_ins.name = request.form['name']
    new_ins.city = request.form['city']
    new_ins.state = request.form['state']
    new_ins.phone = request.form['phone']
    new_ins.image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    new_ins.genres = ",".join(genres)
    new_ins.facebook_link = request.form['facebook_link']
    seeking_description = request.form.get('seeking_description')
    if seeking_description:
        new_ins.website = seeking_description
    website = request.form.get('website')
    if website:
        new_ins.website = website
    seeking_venue = request.form.get('seeking_venue')
    if seeking_venue:
        new_ins.seeking_venue = seeking_venue
    address = request.form.get('address')
    if address:
        new_ins.address = address
    seeking_talent = request.form.get('seeking_talent')
    if seeking_talent:
        new_ins.seeking_talent = seeking_talent
    return new_ins


def update_instance(existing_ins, form):
    existing_ins.name = request.form['name']
    existing_ins.city = request.form['city']
    existing_ins.state = request.form['state']
    existing_ins.phone = request.form['phone']
    existing_ins.image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    existing_ins.genres = ",".join(genres)
    existing_ins.facebook_link = request.form['facebook_link']
    seeking_description = request.form.get('seeking_description')
    if seeking_description:
        existing_ins.website = seeking_description
    website = request.form.get('website')
    if website:
        existing_ins.website = website
    seeking_venue = request.form.get('seeking_venue')
    if seeking_venue:
        existing_ins.seeking_venue = seeking_venue
    address = request.form.get('address')
    if address:
        existing_ins.address = address
    seeking_talent = request.form.get('seeking_talent')
    if seeking_talent:
        existing_ins.seeking_talent = seeking_talent
    return existing_ins


def build_object(existing_artist):
    obj = {
        "id": existing_artist.id,
        "name": existing_artist.name,
        "genres": existing_artist.genres,
        "city": existing_artist.city,
        "state": existing_artist.state,
        "phone": existing_artist.phone,
        "website": existing_artist.website,
        "facebook_link": existing_artist.facebook_link,
        "seeking_venue": existing_artist.seeking_venue,
        "seeking_description": existing_artist.seeking_description,
        "image_link": existing_artist.image_link,
    }

    return obj

    # "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJ
    #     hcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"


def existingInstance(object, id):
    instance = db.session.query(object).get(id)
    if not instance:
        abort(404)
    return instance
