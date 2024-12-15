from __future__ import annotations

from wtforms import HiddenField, SelectField, BooleanField, TextAreaField
from quart_wtf import QuartForm
from wtforms.validators import Length


class ModLogChannel(QuartForm):
    channel = SelectField(
        "Select Channel: ",
        coerce=int,
    )
    choices = HiddenField()


class MemberLogChannel(QuartForm):
    channel = SelectField(
        "Select Channel: ",
        coerce=int,
    )
    choices = HiddenField()


class WelcomeMessage(QuartForm):
    message = TextAreaField(
        "Enter the welcome message, which will be DMed to a new member "
        "on joining the server (Leave blank to disable): ",
        validators=[Length(max=1500)],
    )


class AfkToggle(QuartForm):
    set_afk = BooleanField(
        "Toggle afk: ",
        default=False,
    )

    reason = TextAreaField(
        "Reason for being afk (Optional): ",
        validators=[Length(max=100)],
    )
