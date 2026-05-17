from flask import Blueprint
bp = Blueprint('collaborations', __name__)
from app.collaborations import routes
