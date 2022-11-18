from flask import Blueprint

user_bp = Blueprint('BP', __name__, url_prefix='/user')

from . import view
