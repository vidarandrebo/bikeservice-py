from bikeservice.db import get_db
from flask import g

#return a single bike
def get_bike(id, check_owner=True):
    bike = get_db().execute(
        'SELECT km, b.owner_id, u.id'
        ' FROM bike b JOIN user u ON b.owner_id = u.id'
        ' WHERE b.id = ?',
        (id,)
    ).fetchone()

    if bike is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_owner and bike['owner_id'] != g.user['id']:
        abort(403)

    return bike

#returns a single part
def get_part(id, check_owner=True):
    part = get_db().execute(
        'SELECT km, p.owner_id, u.id, p.bike_id'
        ' FROM part p JOIN user u ON p.owner_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if part is None:
        abort(404, "Part id {0} doesn't exist.".format(id))

    if check_owner and part['owner_id'] != g.user['id']:
        abort(403)

    return part


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

#returns all of the owners bikes
def get_bikes():
    db = get_db()
    bikes = db.execute(
            'SELECT b.id, manufacturer, model, acquired, owner_id, username, km'
            ' FROM bike b JOIN user u ON b.owner_id = u.id'
            ' WHERE b.owner_id = ?'
            ' ORDER BY acquired DESC',str(g.user['id'])
    ).fetchall()
    return bikes

#returns all of the owners parts
def get_parts():
    db = get_db()
    parts = db.execute(
            'SELECT p.id, p.manufacturer, p.model, p.acquired, p.bike_id, b.manufacturer AS bikemanufacturer, b.model AS bikemodel, p.owner_id, u.username, p.km, part_type'
            ' FROM ((part p JOIN user u ON p.owner_id = u.id)'
            ' LEFT JOIN bike b ON p.bike_id = b.id)'
            ' WHERE p.owner_id = ?'
            ' ORDER BY p.acquired DESC',str(g.user['id'])
    ).fetchall()
    return parts

