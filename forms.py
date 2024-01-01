from quart_wtf import QuartForm
from wtforms import SelectField, HiddenField


class ModLogChannel(QuartForm):
    channel = SelectField(
        "Select Channel", coerce=int
    )  # , validators=[DataRequired()])
    choices = HiddenField()


class MemberLogChannel(QuartForm):
    channel = SelectField(
        "Select Channel", coerce=int
    )  # , validators=[DataRequired()])
    choices = HiddenField()
