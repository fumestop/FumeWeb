from __future__ import annotations
from typing import Any

import os
import json
import click

from discord.ext.ipc import Client

from quart import Quart, request, redirect, url_for
from quartcord import DiscordOAuth2Session
from quart_wtf import CSRFProtect

import config

discord: DiscordOAuth2Session = Any
csrf: CSRFProtect = Any

fumeguard_client: Client = Any
fumetune_client: Client = Any
fumetool_client: Client = Any


def create_app() -> Quart:
    app = Quart(__name__, static_url_path="/assets", static_folder="assets")
    app.config.from_pyfile("config.py")

    with open("config.json") as f:
        data = json.load(f)

        if data.get("QUART_ENV") == "development":
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

    global discord, csrf, fumeguard_client, fumetune_client, fumetool_client

    discord = DiscordOAuth2Session(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    fumeguard_client = Client(
        secret_key=config.SECRET_KEY,
        standard_port=config.FUMEGUARD_STANDARD_PORT,
        multicast_port=config.FUMEGUARD_MULTICAST_PORT,
    )

    fumetune_client = Client(
        secret_key=config.SECRET_KEY,
        standard_port=config.FUMETUNE_STANDARD_PORT,
        multicast_port=config.FUMETUNE_MULTICAST_PORT,
    )

    fumetool_client = Client(
        secret_key=config.SECRET_KEY,
        standard_port=config.FUMETOOL_STANDARD_PORT,
        multicast_port=config.FUMETOOL_MULTICAST_PORT,
    )

    @app.before_request
    def _check_maintenance():
        from utils import on_maintenance

        if on_maintenance():
            if request.endpoint in ["meta._maintenance", "static"]:
                return

            return redirect(url_for("meta._maintenance"))

        else:
            if request.endpoint == "meta._maintenance":
                return redirect(url_for("meta._index"))

            return

    @app.cli.command("maintenance")
    @click.argument("state")
    def _maintenance(state: str):
        from utils import on_maintenance, toggle_maintenance

        if state == "enable":
            if on_maintenance():
                click.echo("[WARNING] Application is already on maintenance mode")

            else:
                toggle_maintenance()
                click.echo("[INFO] Maintenance mode enabled")

        elif state == "disable":
            if not on_maintenance():
                click.echo("[WARNING] Application not on maintenance mode")

            else:
                toggle_maintenance()
                click.echo("[INFO] Maintenance mode disabled")

        else:
            click.echo("[USAGE] quart maintenance enable/disable")

    from blueprints.auth import auth_bp
    from blueprints.meta import meta_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.fumeguard import fumeguard_bp
    from blueprints.fumetune import fumetune_bp
    from blueprints.fumetool import fumetool_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(fumeguard_bp)
    app.register_blueprint(fumetune_bp)
    app.register_blueprint(fumetool_bp)

    return app
