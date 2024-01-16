import json

from quart import current_app, redirect, url_for, render_template, flash
from quartcord import Unauthorized, requires_authorization

from blueprints.fumeguard import fumeguard_bp

from forms import ModLogChannel, MemberLogChannel, WelcomeMessage, AfkToggle
from factory import discord, fumeguard_client
from utils import unauthorized


@fumeguard_bp.route("/fumeguard/")
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


@fumeguard_bp.route("/fumeguard/invite/")
async def _invite():
    return redirect(current_app.config["FUMEGUARD_INVITE_URL"])


@fumeguard_bp.route("/fumeguard/vote/")
async def _vote():
    return redirect(current_app.config["FUMEGUARD_VOTE_URL"])


@fumeguard_bp.route("/fumeguard/review/")
async def _review():
    return redirect(current_app.config["FUMEGUARD_REVIEW_URL"])


@fumeguard_bp.route("/fumeguard/app/")
@requires_authorization
async def _app():
    user = await discord.fetch_user()
    return await render_template("fumeguard/app.html", user=user)


@fumeguard_bp.route("/fumeguard/profile/")
@requires_authorization
async def _profile_home():
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["bot_manage_nicknames"]:
            mutual_guilds.pop(_id)

    return await render_template(
        "fumeguard/profile-home.html", user=user, guilds=mutual_guilds
    )


@fumeguard_bp.route("/fumeguard/app/profile/<guild_id>/")
@requires_authorization
async def _profile_guild(guild_id: int):
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["bot_manage_nicknames"]:
            mutual_guilds.pop(_id)

    if guild_id in mutual_guilds.keys():
        guild_id = int(guild_id)

        afk_toggle_form = await AfkToggle().create_form()

        r = await fumeguard_client.request("is_afk", user_id=user.id, guild_id=guild_id)
        is_afk = r.response["afk"]
        afk_details = None

        if is_afk:
            r = await fumeguard_client.request(
                "get_afk_details", user_id=user.id, guild_id=guild_id
            )
            afk_details = r.response["details"]

            afk_toggle_form.set_afk.default = True
            afk_toggle_form.reason.default = afk_details["reason"]
            afk_toggle_form.reason.render_kw = {"disabled": "disabled"}
            afk_toggle_form.process()

        return await render_template(
            "fumeguard/profile-update.html",
            guild_id=guild_id,
            guild_name=mutual_guilds[str(guild_id)]["name"],
            afk_details=afk_details,
            afk_toggle_form=afk_toggle_form,
        )

    else:
        return redirect(url_for("fumeguard._profile_home"))


@fumeguard_bp.route(
    "/fumeguard/app/profile/<guild_id>/update/<route>/", methods=["POST"]
)
@requires_authorization
async def _profile_update(guild_id: str, route: str):
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["bot_manage_nicknames"]:
            mutual_guilds.pop(_id)

    if guild_id in mutual_guilds.keys():
        guild_id = int(guild_id)

        if route == "toggle_afk":
            afk_toggle_form = await AfkToggle().create_form()

            if await afk_toggle_form.validate_on_submit():
                set_afk = afk_toggle_form.set_afk.data
                reason = afk_toggle_form.reason.data or "Unspecified."

                r = await fumeguard_client.request(
                    "is_afk", user_id=user.id, guild_id=guild_id
                )
                is_afk = r.response["afk"]

                if set_afk == is_afk:
                    if is_afk:
                        await flash(
                            "You are already AFK in this server.",
                            "warning",
                        )

                    else:
                        await flash(
                            "You are not AFK in this server.",
                            "warning",
                        )

                    return redirect(
                        url_for("fumeguard._profile_guild", guild_id=guild_id)
                    )

                r = await fumeguard_client.request(
                    "toggle_afk", user_id=user.id, guild_id=guild_id, reason=reason
                )

                if r.response["status"] == 200:
                    await flash("AFK status has been updated.", "success")
                    return redirect(
                        url_for("fumeguard._profile_guild", guild_id=guild_id)
                    )

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(
                        url_for("fumeguard._profile_guild", guild_id=guild_id)
                    )

        else:
            return redirect(url_for("fumeguard._profile_home"))


@fumeguard_bp.route("/fumeguard/settings/")
@requires_authorization
async def _settings_home():
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["member_manage_guild"]:
            mutual_guilds.pop(_id)

    return await render_template(
        "fumeguard/settings-home.html", user=user, guilds=mutual_guilds
    )


@fumeguard_bp.route("/fumeguard/app/settings/<guild_id>/")
@requires_authorization
async def _settings_guild(guild_id: str):
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["member_manage_guild"]:
            mutual_guilds.pop(_id)

    if guild_id in mutual_guilds.keys():
        guild_id = int(guild_id)

        r = await fumeguard_client.request("get_channel_list", guild_id=guild_id)

        if "error" in r.response:
            return redirect(url_for("fumeguard._settings_home"))

        channels = list()

        for _id, _name in r.response["channels"].items():
            channels.append((_id, f"# {_name}"))

        channels.insert(0, (0, "DISABLE LOGGING"))

        # Moderation Logging Form
        mod_log_form = await ModLogChannel().create_form()
        mod_log_form.channel.choices = channels

        r = await fumeguard_client.request("get_mod_log_channel", guild_id=guild_id)
        current_mod_log_channel = r.response

        if current_mod_log_channel["id"] == 0:
            current_mod_log_channel = "MODERATION LOG DISABLED"

        else:
            mod_log_form.channel.default = current_mod_log_channel["id"]
            mod_log_form.process()
            current_mod_log_channel = f"# {current_mod_log_channel['name']}"

        r = await fumeguard_client.request("get_member_log_channel", guild_id=guild_id)
        current_member_log_channel = r.response

        mod_log_form.choices.data = json.dumps(channels)

        # Member Logging Form
        member_log_form = await MemberLogChannel().create_form()
        member_log_form.channel.choices = channels

        if current_member_log_channel["id"] == 0:
            current_member_log_channel = "MEMBER LOG DISABLED"

        else:
            member_log_form.channel.default = current_member_log_channel["id"]
            member_log_form.process()
            current_member_log_channel = f"# {current_member_log_channel['name']}"

        member_log_form.choices.data = json.dumps(channels)

        # Welcome Message Form
        welcome_message_form = await WelcomeMessage().create_form()

        r = await fumeguard_client.request("get_welcome_message", guild_id=guild_id)
        current_welcome_message = r.response

        welcome_message_form.message.default = current_welcome_message["message"] or ""
        welcome_message_form.process()

        return await render_template(
            "fumeguard/settings-update.html",
            guild_id=guild_id,
            guild_name=mutual_guilds[str(guild_id)]["name"],
            mod_log_form=mod_log_form,
            member_log_form=member_log_form,
            welcome_message_form=welcome_message_form,
            current_mod_log_channel=current_mod_log_channel,
            current_member_log_channel=current_member_log_channel,
        )

    else:
        return redirect(url_for("fumeguard._settings_home"))


@fumeguard_bp.route(
    "/fumeguard/app/settings/<guild_id>/update/<route>/", methods=["POST"]
)
@requires_authorization
async def _settings_update(guild_id: int, route: str):
    user = await discord.fetch_user()

    r = await fumeguard_client.request("get_mutual_guilds", user_id=user.id)
    mutual_guilds = r.response["guilds"]

    for _id, _details in mutual_guilds.copy().items():
        if not _details["member_manage_guild"]:
            mutual_guilds.pop(_id)

    if guild_id in mutual_guilds.keys():
        guild_id = int(guild_id)

        if route == "mod_log_channel":
            mod_log_form = await ModLogChannel().create_form()

            channels = json.loads(mod_log_form.choices.data)
            mod_log_form.channel.choices = channels

            if await mod_log_form.validate_on_submit():
                channel_id = int(mod_log_form.channel.data)

                r = await fumeguard_client.request(
                    "get_mod_log_channel", guild_id=guild_id
                )
                current_mod_log_channel = r.response["id"]

                if channel_id == current_mod_log_channel:
                    await flash(
                        "The channel you selected is already the current moderation log channel.",
                        "warning",
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                r = await fumeguard_client.request(
                    "update_mod_log_channel", guild_id=guild_id, channel_id=channel_id
                )

                if r.response["status"] == 200:
                    await flash("Moderation log channel has been updated.", "success")
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

        elif route == "member_log_channel":
            member_log_form = await MemberLogChannel().create_form()

            channels = json.loads(member_log_form.choices.data)
            member_log_form.channel.choices = channels

            if await member_log_form.validate_on_submit():
                channel_id = int(member_log_form.channel.data)

                r = await fumeguard_client.request(
                    "get_member_log_channel", guild_id=guild_id
                )
                current_member_log_channel = r.response["id"]

                if channel_id == current_member_log_channel:
                    await flash(
                        "The channel you selected is already the current member log channel.",
                        "warning",
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                r = await fumeguard_client.request(
                    "update_member_log_channel",
                    guild_id=guild_id,
                    channel_id=channel_id,
                )

                if r.response["status"] == 200:
                    await flash("Member log channel has been updated.", "success")
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

        elif route == "welcome_message":
            welcome_message_form = await WelcomeMessage().create_form()

            if await welcome_message_form.validate_on_submit():
                message = welcome_message_form.message.data or None

                r = await fumeguard_client.request(
                    "get_welcome_message", guild_id=guild_id
                )
                current_welcome_message = r.response["message"]

                if message == current_welcome_message:
                    await flash(
                        "The message you entered is already the current welcome message.",
                        "warning",
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                r = await fumeguard_client.request(
                    "update_welcome_message",
                    guild_id=guild_id,
                    message=message,
                )

                if r.response["status"] == 200:
                    await flash("Welcome message has been updated.", "success")
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

                else:
                    await flash(
                        "An error occurred while processing your request.", "error"
                    )
                    return redirect(
                        url_for("fumeguard._settings_guild", guild_id=guild_id)
                    )

        else:
            return redirect(url_for("fumeguard._settings_guild", guild_id=guild_id))

    else:
        return redirect(url_for("fumeguard._settings_home"))


# noinspection PyUnusedLocal
@fumeguard_bp.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("auth._login"))
