from flask import request, abort
from app import db


def update_instance(instance_var, form, attrs):
    """
    update_instance takes in a instance variables and fill all of its attributes with given form data
    :param instance_var: instance variable
    :param form: form instance
    :param attrs: [attributes to be set]
    :return: instance variable
    """
    for attr in attrs:
        if attr == 'genres':
            attr_val = ','.join(request.form.getlist(attr))
        else:
            attr_val = request.form.get(attr)
        # Update attributes with new updated value if a new value is given
        if attr_val and getattr(instance_var, attr) != attr_val:
            setattr(instance_var, attr, attr_val)
    return instance_var


def set_form_data(form_ins, instance_var):
    """
    set_form_data takes in a form instance and sets its attributes with the
    :param form_ins: form instance
    :param instance_var: instance variable
    :return: form instance
    """
    form_ins.name.data = instance_var.name
    form_ins.city.data = instance_var.city
    form_ins.state.data = instance_var.state
    form_ins.phone.data = instance_var.phone
    form_ins.image_link.data = instance_var.image_link
    genres = instance_var.genres
    form_ins.genres.data = genres.split(",")
    form_ins.facebook_link.data = instance_var.facebook_link

    if hasattr(form_ins, "seeking_description"):
        form_ins.seeking_description.data = instance_var.seeking_description

    if hasattr(form_ins, "website"):
        form_ins.website.data = instance_var.website

    if hasattr(instance_var, "seeking_venue") and hasattr(form_ins, "seeking_venue"):
        form_ins.seeking_venue.data = instance_var.seeking_venue

    if hasattr(instance_var, "address") and hasattr(form_ins, "address"):
        form_ins.address.data = instance_var.address

    if hasattr(instance_var, "seeking_talent") and hasattr(form_ins, "seeking_talent"):
        form_ins.seeking_talent.data = instance_var.seeking_talent

    return form_ins
