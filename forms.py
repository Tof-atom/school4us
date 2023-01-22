from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length, Regexp, ValidationError


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    firstName = StringField('firstName')
    lastName = StringField('lastName')
    motherName = StringField('motherName')
    fatherName = StringField('fatherName')
    gender = StringField('gender')
    username = StringField('username',
                           validators=[InputRequired(),
                                       Length(4, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must start with a letter and must have only letters, numbers, dots or underscores')]
                           )
    email = EmailField('email', validators=[InputRequired(), Email()])
    # TODO: password length 8 char
    password = PasswordField('password', validators=[InputRequired(), Length(8)])
    password2 = PasswordField('password2',
                              validators=[InputRequired(),
                                          EqualTo('password',
                                                  message='Passwords must match.')])
    submit = SubmitField('Signin')
    #
    # def validate_password(self, field):
    #     with open('data/common_passwords.txt') as f:
    #         for line in f.readlines():
    #             if field.data == line.strip():
    #                 raise ValidationError('Your password is too common.')

    # Validator for username
    # validators = [InputRequired(),
    #               Length(4, 64),
    #               Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    #                      'Usernames must start with a letter and must have only letters, numbers, dots or underscores')]

    # Validator for password
    # , validators = [InputRequired(), Length(8)]