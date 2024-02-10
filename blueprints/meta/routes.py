from quart import render_template, redirect, current_app

from . import meta_bp

from utils import unauthorized


@meta_bp.route("/")
async def _index():
    return await render_template("meta/index.html", unauthorized=unauthorized())


@meta_bp.route("/premium/")
async def _premium():
    return await render_template("meta/premium.html", unauthorized=unauthorized())


@meta_bp.route("/community/")
async def _community():
    return redirect(current_app.config["COMMUNITY_INVITE_URL"])


@meta_bp.route("/terms/")
async def _terms():
    return await render_template("meta/terms.html", unauthorized=unauthorized())


@meta_bp.route("/privacy/")
async def _privacy():
    return await render_template("meta/privacy.html", unauthorized=unauthorized())


@meta_bp.route("/maintenance/")
async def _maintenance():
    return await render_template("meta/maintenance.html", maintenance=True), 503
