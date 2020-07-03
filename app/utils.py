from flask import request, abort
from app import db


def update_instance(instance_var, form, attrs):
    for attr in attrs:
        if attr == 'genres':
            attr_val = ','.join(request.form.getlist(attr))
        else:
            attr_val = request.form.get(attr)
        # Update attributes with new updated value if a new value is given
        if attr_val:
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
