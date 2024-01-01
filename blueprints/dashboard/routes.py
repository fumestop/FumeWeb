from quart import redirect, url_for, render_template
from quartcord import Unauthorized, requires_authorization

from blueprints.dashboard import dashboard_bp

from factory import discord


@dashboard_bp.route("/app")
@requires_authorization
async def _app():
    user = await discord.fetch_user()
    return await render_template("dashboard/app.html", user=user)


# noinspection PyUnusedLocal
@dashboard_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
