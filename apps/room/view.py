from flask import Blueprint, render_template, request
from exts import db
from apps.room.model import Room

room_bp = Blueprint('room', __name__, url_prefix='/room/')


@room_bp.route('/roomInfo/')
def room_fn():
    rooms = db.session.query(Room).all()
    return render_template('room/roomInfo.html', rooms=rooms)
