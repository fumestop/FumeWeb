from quart import Blueprint

fumetool_bp = Blueprint("fumetool", __name__)

from . import routes
