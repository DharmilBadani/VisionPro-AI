"""
Authentication Forms
VisionAI Pro
"""

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class LoginForm(FlaskForm):
    """
    User Login Form
    """

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    remember_me = BooleanField(
        "Remember Me"
    )

    submit = SubmitField(
        "Login"
    )


class RegisterForm(FlaskForm):
    """
    User Registration Form
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100
            )
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=128
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Create Account"
    )