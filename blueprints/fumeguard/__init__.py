from quart import Blueprint

fumeguard_bp = Blueprint("fumeguard", __name__)

from . import routes
