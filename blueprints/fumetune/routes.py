from quart import current_app, redirect, url_for, render_template
from quartcord import Unauthorized, requires_authorization

from blueprints.fumetune import fumetune_bp

from factory import fumetune_client
from utils import unauthorized


@fumetune_bp.route("/fumetune")
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


@fumetune_bp.route("/fumetune/invite")
async def _invite():
    return redirect(current_app.config["FUMETUNE_INVITE_URL"])


@fumetune_bp.route("/fumetune/app")
@requires_authorization
async def _app():
    return await render_template("fumetune/app.html")


# noinspection PyUnusedLocal
@fumetune_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
