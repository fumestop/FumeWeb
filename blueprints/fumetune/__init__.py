from quart import Blueprint

fumetune_bp = Blueprint("fumetune", __name__)

from . import routes
