from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Local development reads from a gitignored .env at the repo root. In
# production the environment is populated by Doppler and no .env exists, so
# load_dotenv is a harmless no-op.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    @staticmethod
    def _get_from_env(name: str) -> str:
        try:
            return os.environ[name]
        except KeyError:
            raise RuntimeError(
                f"Missing required config {name!r} "
                "(set it in .env for local development, or Doppler in production)"
            ) from None

    SECRET_KEY: str = _get_from_env("SECRET_KEY")

    DISCORD_CLIENT_ID: int = int(_get_from_env("DISCORD_CLIENT_ID"))
    DISCORD_CLIENT_SECRET: str = _get_from_env("DISCORD_CLIENT_SECRET")
    DISCORD_REDIRECT_URI: str = _get_from_env("DISCORD_REDIRECT_URI")
    DISCORD_BOT_TOKEN: str = _get_from_env("DISCORD_BOT_TOKEN")

    COMMUNITY_GUILD_ID: int = int(_get_from_env("COMMUNITY_GUILD_ID"))
    COMMUNITY_INVITE_URL: str = _get_from_env("COMMUNITY_INVITE_URL")

    FUMEGUARD_STANDARD_PORT: int = int(_get_from_env("FUMEGUARD_STANDARD_PORT"))
    FUMEGUARD_MULTICAST_PORT: int = int(_get_from_env("FUMEGUARD_MULTICAST_PORT"))
    FUMEGUARD_INVITE_URL: str = _get_from_env("FUMEGUARD_INVITE_URL")
    FUMEGUARD_VOTE_URL: str = _get_from_env("FUMEGUARD_VOTE_URL")
    FUMEGUARD_REVIEW_URL: str = _get_from_env("FUMEGUARD_REVIEW_URL")

    FUMETUNE_STANDARD_PORT: int = int(_get_from_env("FUMETUNE_STANDARD_PORT"))
    FUMETUNE_MULTICAST_PORT: int = int(_get_from_env("FUMETUNE_MULTICAST_PORT"))
    FUMETUNE_INVITE_URL: str = _get_from_env("FUMETUNE_INVITE_URL")
    FUMETUNE_VOTE_URL: str = _get_from_env("FUMETUNE_VOTE_URL")
    FUMETUNE_REVIEW_URL: str = _get_from_env("FUMETUNE_REVIEW_URL")

    FUMETOOL_STANDARD_PORT: int = int(_get_from_env("FUMETOOL_STANDARD_PORT"))
    FUMETOOL_MULTICAST_PORT: int = int(_get_from_env("FUMETOOL_MULTICAST_PORT"))
    FUMETOOL_INVITE_URL: str = _get_from_env("FUMETOOL_INVITE_URL")
    FUMETOOL_VOTE_URL: str = _get_from_env("FUMETOOL_VOTE_URL")
    FUMETOOL_REVIEW_URL: str = _get_from_env("FUMETOOL_REVIEW_URL")

    TEMPLATES_AUTO_RELOAD: bool = _get_from_env("TEMPLATES_AUTO_RELOAD").lower() in (
        "true",
        "1",
        "yes",
    )
