from flask import request, abort
from app import db


# def create_instance(model, form):
#     """
#     :param model: Venue or Artist class
#     :param form: Form instance
#     :return: Instance of the the model
#     """
#     new_ins = model()
#     new_ins.name = request.form['name']
#     new_ins.city = request.form['city']
#     new_ins.state = request.form['state']
#     new_ins.phone = request.form['phone']
#     new_ins.image_link = request.form.get('image_link')
#     genres = request.form.getlist('genres')
#     new_ins.genres = ",".join(genres)
#     new_ins.facebook_link = request.form['facebook_link']
#     seeking_description = request.form.get('seeking_description')
#     if seeking_description:
#         new_ins.website = seeking_description
#     website = request.form.get('website')
#     if website:
#         new_ins.website = website
#     seeking_venue = request.form.get('seeking_venue')
#     if seeking_venue:
#         new_ins.seeking_venue = seeking_venue
#     address = request.form.get('address')
#     if address:
#         new_ins.address = address
#     seeking_talent = request.form.get('seeking_talent')
#     if seeking_talent:
#         new_ins.seeking_talent = seeking_talent
#     return new_ins


def update_instance(instance_var, form, attrs):
    for attr in attrs:
        if attr == 'genres':
            attr_val = ','.join(request.form.getlist(attr))
        else:
            attr_val = request.form.get(attr)
        # Update attributes with new updated value
        if getattr(instance_var, attr) != attr_val:
            setattr(instance_var, attr, attr_val)
    return instance_var


def set_form_data(form_ins, obj):
    form_ins.name.data = obj.name
    form_ins.city.data = obj.city
    form_ins.state.data = obj.state
    form_ins.phone.data = obj.phone
    form_ins.image_link.data = obj.image_link
    genres = obj.genres
    form_ins.genres.data = genres.split(",")
    form_ins.facebook_link.data = obj.facebook_link
    if hasattr(form_ins, "seeking_description"):
        form_ins.seeking_description.data = obj.seeking_description

    if hasattr(form_ins, "website"):
        form_ins.website.data = obj.website

    if hasattr(obj, "seeking_venue") and hasattr(form_ins, "seeking_venue"):
        form_ins.seeking_venue.data = obj.seeking_venue

    if hasattr(obj, "address") and hasattr(form_ins, "address"):
        form_ins.address.data = obj.address

    if hasattr(obj, "seeking_talent") and hasattr(form_ins, "seeking_talent"):
        form_ins.seeking_talent.data = obj.seeking_talent

    return form_ins
