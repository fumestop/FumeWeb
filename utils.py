from __future__ import annotations
from typing import Optional

import json

from factory import discord


def on_maintenance(return_data: Optional[bool] = False) -> bool | dict[str, bool]:
    with open("config.json") as f:
        data = json.load(f)

    if return_data:
        return data

    return data.get("MAINTENANCE")


def toggle_maintenance() -> None:
    data = on_maintenance(return_data=True)

    with open("config.json", "w") as f:
        data["MAINTENANCE"] = not data["MAINTENANCE"]
        json.dump(data, f, indent=4)


def logged_in() -> bool:
    return True if discord.user_id else False


def unauthorized() -> bool:
    return not logged_in()
