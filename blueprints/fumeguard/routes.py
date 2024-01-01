import json

from quart import current_app, redirect, url_for, render_template, flash
from quartcord import Unauthorized, requires_authorization

from blueprints.fumeguard import fumeguard_bp

from forms import ModLogChannel, MemberLogChannel
from factory import discord, fumeguard_client
from utils import unauthorized


@fumeguard_bp.route("/fumeguard")
async def _index():
    r = await fumeguard_client.request("get_guild_count")
    server_count = r.response["count"]
    r = await fumeguard_client.request("get_user_count")
    user_count = r.response["count"]
    r = await fumeguard_client.request("get_command_count")
    command_count = r.response["count"]

    return await render_template(
        "fumeguard/index.html",
        unauthorized=unauthorized(),
        server_count=server_count,
        user_count=user_count,
        command_count=command_count,
    )


@fumeguard_bp.route("/fumeguard/invite")
async def _invite():
    return redirect(current_app.config["FUMEGUARD_INVITE_URL"])


@fumeguard_bp.route("/fumeguard/app")
@requires_authorization
async def _app():
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    guilds = list()

    for guild in await user.get_guilds():
        if guild.permissions.manage_guild and guild.id in mutual_guilds:
            guilds.append([guild.id, guild.name])

    return await render_template(
        "fumeguard/app.html", user=user, guilds=guilds
    )


@fumeguard_bp.route("/fumeguard/app/settings/<guild_id>")
@requires_authorization
async def _settings(guild_id):
    try:
        guild_id = int(guild_id)

    except ValueError:
        return redirect(url_for("fumeguard._app"))

    user = await discord.fetch_user()

    guilds = list()

    for guild in await user.get_guilds():
        if guild.permissions.manage_guild:
            guilds.append(guild.id)

    if guild_id in guilds:
        r = await fumeguard_client.request("get_channel_list", guild_id=guild_id)

        if "error" in r.response:
            return redirect(url_for("fumeguard._app"))

        channels = list()

        for _channel in r.response["channels"]:
            channels.append((_channel["id"], f"#{_channel['name']}"))

        channels.insert(0, (0, "LOGGING DISABLED"))

        mod_log_form = await ModLogChannel().create_form()
        member_log_form = await MemberLogChannel().create_form()

        mod_log_form.channel.choices = channels
        member_log_form.channel.choices = channels

        r = await fumeguard_client.request("get_mod_log_channel", guild_id=guild_id)
        current_mod_log_channel = r.response
        r = await fumeguard_client.request("get_member_log_channel", guild_id=guild_id)
        current_member_log_channel = r.response

        if "error" in current_mod_log_channel:
            current_mod_log_channel = "MODERATION LOG DISABLED"

        else:
            for channel in channels:
                if channel[0] == current_mod_log_channel["id"]:
                    mod_log_form.channel.default = channel[0]
                    mod_log_form.process()
                    break

            current_mod_log_channel = f"#{current_mod_log_channel['name']}"

        if "error" in current_member_log_channel:
            current_member_log_channel = "MEMBER LOG DISABLED"

        else:
            for channel in channels:
                if channel[0] == current_member_log_channel["id"]:
                    member_log_form.channel.default = channel[0]
                    member_log_form.process()
                    break

            current_member_log_channel = f"#{current_member_log_channel['name']}"

        mod_log_form.choices.data = json.dumps(channels)
        member_log_form.choices.data = json.dumps(channels)

        return await render_template(
            "fumeguard/settings.html",
            guild_id=guild_id,
            mod_log_form=mod_log_form,
            member_log_form=member_log_form,
            current_mod_log_channel=current_mod_log_channel,
            current_member_log_channel=current_member_log_channel,
        )

    else:
        return redirect(url_for("fumeguard._app"))


@fumeguard_bp.route(
    "/fumeguard/app/settings/<guild_id>/update/<route>", methods=["POST"]
)
@requires_authorization
async def _update(guild_id, route):
    try:
        guild_id = int(guild_id)

    except ValueError:
        return redirect(url_for("fumeguard._app"))

    user = await discord.fetch_user()

    guilds = list()

    for guild in await user.get_guilds():
        if guild.permissions.manage_guild:
            guilds.append(guild.id)

    if guild_id in guilds:
        if route == "mod_log_channel":
            mod_log_form = await ModLogChannel().create_form()

            channels = json.loads(mod_log_form.choices.data)
            mod_log_form.channel.choices = channels

            if await mod_log_form.validate_on_submit():
                channel_id = int(mod_log_form.channel.data)

                r = await fumeguard_client.request(
                    "update_mod_log_channel", guild_id=guild_id, channel_id=channel_id
                )

                if r.response["status"] == 200:
                    await flash("Moderation log channel has been updated.", "success")
                    return redirect(url_for("fumeguard._settings", guild_id=guild_id))

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(url_for("fumeguard._settings", guild_id=guild_id))

        elif route == "member_log_channel":
            member_log_form = await MemberLogChannel().create_form()

            channels = json.loads(member_log_form.choices.data)
            member_log_form.channel.choices = channels

            if await member_log_form.validate_on_submit():
                channel_id = int(member_log_form.channel.data)

                r = await fumeguard_client.request(
                    "update_member_log_channel",
                    guild_id=guild_id,
                    channel_id=channel_id,
                )

                if r.response["status"] == 200:
                    await flash("Member log channel has been updated.", "success")
                    return redirect(url_for("fumeguard._settings", guild_id=guild_id))

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(url_for("fumeguard._settings", guild_id=guild_id))

        else:
            return redirect(url_for("fumeguard._settings", guild_id=guild_id))

    else:
        return redirect(url_for("fumeguard._app"))


# noinspection PyUnusedLocal
@fumeguard_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
