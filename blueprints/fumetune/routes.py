from quart import url_for, redirect, current_app, render_template
from quartcord import Unauthorized, requires_authorization

from utils import unauthorized
from factory import fumetune_client

from . import fumetune_bp


@fumetune_bp.route("/fumetune/")
async def _index():
    r = await fumetune_client.request("get_guild_count")
    server_count = r.response["count"]
    r = await fumetune_client.request("get_user_count")
    user_count = r.response["count"]
    r = await fumetune_client.request("get_command_count")
    command_count = r.response["count"]

    return await render_template(
        "fumetune/index.html",
        unauthorized=unauthorized(),
        server_count=server_count,
        user_count=user_count,
        command_count=command_count,
    )


@fumetune_bp.route("/fumetune/invite/")
async def _invite():
    return redirect(current_app.config["FUMETUNE_INVITE_URL"])


@fumetune_bp.route("/fumetune/vote/")
async def _vote():
    return redirect(current_app.config["FUMETUNE_VOTE_URL"])


@fumetune_bp.route("/fumetune/review/")
async def _review():
    return redirect(current_app.config["FUMETUNE_REVIEW_URL"])


@fumetune_bp.route("/fumetune/app/")
@requires_authorization
async def _app():
    return await render_template("fumetune/app.html")


# noinspection PyUnusedLocal
@fumetune_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
