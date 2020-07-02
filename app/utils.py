from flask import request


def create_instance(model, form):
    new_ins = model()
    new_ins.name = request.form['name']
    new_ins.city = request.form['city']
    new_ins.state = request.form['state']
    address = request.form.get('address')
    if address:
        new_ins.address = address
    new_ins.phone = request.form['phone']
    new_ins.image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    new_ins.genres = ",".join(genres)
    new_ins.facebook_link = request.form['facebook_link']
    seeking_venue = request.form.get('seeking_venue')
    if seeking_venue:
        new_ins.seeking_venue = seeking_venue
    website = request.form.get('website')
    if website:
        new_ins.website = website
    return new_ins
