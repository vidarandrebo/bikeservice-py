from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bikeservice.auth import login_required
from bikeservice.db import get_db
from bikeservice.db_functions import get_bike, get_part, get_bikes, get_parts, get_nparts, get_nbikes, get_total_km

bp = Blueprint('bikeservice',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, p.created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY p.created DESC'
    ).fetchall()
    return render_template('bikeservice/index.html', posts=posts)

@bp.route('/user')
@login_required
def user():
    return render_template('bikeservice/user.html', n_parts=get_nparts(), n_bikes=get_nbikes(), distance=get_total_km())

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
    return render_template('bikeservice/bikes.html', bike_list=get_bikes())

@bp.route('/parts', methods=('GET', 'POST'))
@login_required
def parts():
    return render_template('bikeservice/parts.html', part_list=get_parts())

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

@bp.route('/<int:id>/update_part', methods=('GET', 'POST'))
@login_required
def update_part(id):
    if request.method == 'POST':
        km = request.form['km']
        bike = request.form['bike']
        error = None
        if not km:
            error = 'Km is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'UPDATE part SET km = ?, bike_id = ?'
                    ' WHERE id = ?',
                    (km, bike, id)
            )
            db.commit()
            return redirect(url_for('bikeservice.parts'))
    return render_template('bikeservice/update_part.html', part=get_part(id), bikes=get_bikes())

@bp.route('/<int:id>/update_bike', methods=('GET', 'POST'))
@login_required
def update_bike(id):
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
    return render_template('bikeservice/update_bike.html', bike=get_bike(id))
