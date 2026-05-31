from __future__ import annotations

import sys
import asyncio
import logging
from datetime import datetime

import discord

from factory import create_app

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

else:
    # noinspection PyUnresolvedReferences
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup_logging() -> None:
    log = logging.getLogger()

    # Console handler (coloured automatically when attached to a TTY).
    stream_handler = logging.StreamHandler()
    discord.utils.setup_logging(handler=stream_handler, level=logging.INFO)

    # File handler, mirroring the console with the same format discord uses.
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    file_handler = logging.FileHandler(
        filename=f"logs/fumeweb-{datetime.now().strftime('%Y-%m-%d~%H-%M-%S')}.log",
        encoding="utf-8",
        mode="w",
    )
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    logging.getLogger("discord").setLevel(logging.INFO)
    logging.getLogger("discord.http").setLevel(logging.WARNING)

    log.setLevel(logging.INFO)


setup_logging()

app = create_app()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.run(loop=loop)
