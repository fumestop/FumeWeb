from quart import url_for, redirect, current_app, render_template
from quartcord import Unauthorized, requires_authorization

from utils import unauthorized
from factory import fumetool_client

from . import fumetool_bp


@fumetool_bp.route("/fumetool/")
async def _index():
    r = await fumetool_client.request("get_guild_count")
    server_count = r.response["count"]
    r = await fumetool_client.request("get_user_count")
    user_count = r.response["count"]
    r = await fumetool_client.request("get_command_count")
    command_count = r.response["count"]

    return await render_template(
        "fumetool/index.html",
        unauthorized=unauthorized(),
        server_count=server_count,
        user_count=user_count,
        command_count=command_count,
    )


@fumetool_bp.route("/fumetool/invite/")
async def _invite():
    return redirect(current_app.config["FUMETOOL_INVITE_URL"])


@fumetool_bp.route("/fumetool/vote/")
async def _vote():
    return redirect(current_app.config["FUMETOOL_VOTE_URL"])


@fumetool_bp.route("/fumetool/review/")
async def _review():
    return redirect(current_app.config["FUMETOOL_REVIEW_URL"])


@fumetool_bp.route("/fumetool/app/")
@requires_authorization
async def _app():
    return await render_template("fumetool/app.html")


# noinspection PyUnusedLocal
@fumetool_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
