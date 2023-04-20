from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from oasis_nourish.models import User
import phonenumbers


class EditPersonalDetailsForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(1, 64)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update Details')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data, "ZA")
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class EditEmailForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Update Email")


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('new_password2', message='Passwords must match'), Length(8, 16)
    ])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Change password')
