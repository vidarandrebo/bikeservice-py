from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bikeservice.auth import login_required
from bikeservice.db import get_db

bp = Blueprint('bikeservice',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
    ).fetchall()
    return render_template('bikeservice/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO post (title, body, author_id)'
                    ' VALUES (?, ?, ?)',
                    (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('bikeservice.index'))
    return render_template('bikeservice/create.html')

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

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'UPDATE post SET title = ?, body = ?'
                    ' WHERE id = ?',
                    (title, body, id)
            )
            db.commit()
            return redirect(url_for('bikeservice.index'))
    return render_template('bikeservice/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('bikeservice.index'))

@bp.route('/bikes', methods=('GET', 'POST'))
@login_required
def bikes():
    db = get_db()
    posts = db.execute(
            'SELECT b.id, manufacturer, model, acquired, owner_id, username, km'
            ' FROM bike b JOIN user u ON b.owner_id = u.id'
            ' WHERE b.owner_id = ?'
            ' ORDER BY acquired DESC',str(g.user['id'])
    ).fetchall()
    return render_template('bikeservice/bikes.html', posts=posts)

@bp.route('/parts', methods=('GET', 'POST'))
@login_required
def parts():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, manufacturer, model, acquired, bike_id, owner_id, username, km, part_type'
            ' FROM part p JOIN user u ON p.owner_id = u.id'
            ' WHERE p.owner_id = ?'
            ' ORDER BY acquired DESC',str(g.user['id'])
    ).fetchall()
    return render_template('bikeservice/parts.html', posts=posts)

@bp.route('/create_bike', methods=('GET', 'POST'))
@login_required
def create_bike():
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        acquired = request.form['acquired']
        km = request.form['km']
        error = None
        if not manufacturer:
            error = 'Manufacturer is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO bike (manufacturer, model, owner_id, acquired, km)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (manufacturer, model, g.user['id'], acquired, km)
            )
            db.commit()
            return redirect(url_for('bikeservice.bikes'))
    return render_template('bikeservice/create_bike.html')

@bp.route('/create_part', methods=('GET', 'POST'))
@login_required
def create_part():
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        part_type = request.form['part_type']
        acquired = request.form['acquired']
        km = request.form['km']
        error = None
        if not manufacturer:
            error = 'Manufacturer is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO part (manufacturer, model, owner_id, acquired, km, part_type)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (manufacturer, model, g.user['id'], acquired, km, part_type)
            )
            db.commit()
            return redirect(url_for('bikeservice.parts'))
    return render_template('bikeservice/create_part.html')

@bp.route('/<int:id>/update_km', methods=('GET', 'POST'))
@login_required
def update_km(id):
    bike = get_bike(id)

    if request.method == 'POST':
        km = request.form['km']
        error = None

        if not km:
            error = 'Km is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'UPDATE bike SET km = ?'
                    ' WHERE id = ?',
                    (km, id)
            )
            db.commit()
            return redirect(url_for('bikeservice.bikes'))
    return render_template('bikeservice/update_km.html', post=bike)

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
