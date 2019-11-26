from flask import Blueprint

bp = Blueprint('main', __name__)

from cirean.main import views