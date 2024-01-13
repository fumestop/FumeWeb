from quart import redirect, url_for, current_app, flash
from quartcord import AccessDenied

from blueprints.auth import auth_bp

from factory import discord
from utils import logged_in


@auth_bp.route("/login/")
async def _login():
    if logged_in():
        return redirect(url_for("dashboard._app"))

    return await discord.create_session(
        scope=["identify", "guilds", "guilds.join"]
    )  # , prompt=False)


@auth_bp.route("/logout/")
async def _logout():
    discord.revoke()
    await flash("You have been successfully logged out.", "success")
    return redirect(url_for("meta._index"))


@auth_bp.route("/callback/")
async def _callback():
    try:
        await discord.callback()

    except AccessDenied:
        await flash("You cancelled the request to login.", "error")
        return redirect(url_for("meta._index"))

    await flash("You have successfully logged in.", "success")

    user = await discord.fetch_user()
    m = await user.add_to_guild(current_app.config["COMMUNITY_SERVER_ID"])

    if m:
        await flash(
            f"You have been added to our community server!",
            "success",
        )

    return redirect(url_for("dashboard._app"))
