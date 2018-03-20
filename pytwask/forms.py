# -*- coding: utf-8 -*-

'''
Courtesy of http://flask.pocoo.org/snippets/64/
'''

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo,\
    ValidationError

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def check_login_credentials(self):
        """
        Check the login credentials (username, password).
        """
        # TODO: Check the login credentials (username, password) match 
        # the record in the backend database.
        if self.username.data == 'renwei' and self.password.data == '111111':
            return True
        else:
            return False
        
class SignUpForm(FlaskForm):
    username = StringField('Username', 
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters, '
                                    '    and underscores.')])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
            
    def validate_username(self, username_field):
        if False: # TODO: Check if the username is already taken in the backend database.
            raise ValidationError('This username is already taken.')
        
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', 
                                 validators=[
                                 DataRequired(),
                                 EqualTo('new_password2', message='New passwords must match')])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    
    def validate_old_password(self, old_password_field):
        if False: # TODO: Validate the old password in the backend database.
            raise ValidationError('Incorrect old password.')

class PostTweetForm(FlaskForm):
    tweet = StringField('Tweet', validators=[DataRequired()])