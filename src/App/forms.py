from string import whitespace
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from App import db
import re



class SignupForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="This field cannot be empty."),
                                       Length(min=3, max=15, message="This field's length is from 3 to 15 characters.")])

    email = StringField(label="Email",
                           validators=[DataRequired(message="This field cannot be empty."), 
                                       Email(message="Please insert a valid email.")])

    password = StringField(label="Password",
                           validators=[DataRequired(message="This field cannot be empty."),
                                       Length(min=3, max=15, message="This field's length is from 3 to 15 characters.")])
    
    password2 = StringField(label="Re-type Password",
                           validators=[DataRequired(message="This field cannot be empty."),
                                       Length(min=3, max=15, message="This field's length is from 3 to 15 characters."),
                                       EqualTo('password', message='Passwords should match.')])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user_exists = db.user.find_one({"username": re.compile(f'^{username.data}$', re.IGNORECASE)})
        if user_exists:
            raise ValidationError('This username is already in use!')
    
    def validate_email(self, email):
        email_exists = db.user.find_one({"email": re.compile(f'^{email.data}$', re.IGNORECASE)})
        if email_exists:
            raise ValidationError('This email is already in use!')


class LoginForm(FlaskForm):
 
    email = StringField(label="Email",
                           validators=[DataRequired(message="This field cannot be empty."), 
                                       Email(message="Please insert a valid email.")])

    password = StringField(label="Password",
                           validators=[DataRequired(message="This field cannot be empty.")])
    submit = SubmitField('Login')


class NewFeedbackForm(FlaskForm):
    feedback_title = StringField(label="Feedback Title",
                           validators=[DataRequired(message="This field cannot be empty."),
                                       Length(min=3, max=50, message="This field's length is from 3 to 15 characters.")])

    feedback_body = TextAreaField(label="Feeback Text",
                           validators=[DataRequired(message="This field cannot be empty."), 
                                       Length(min=5, message="This field needs to contain at least 5 characters")])
    submit = SubmitField('Send')

class UploadImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[DataRequired(message="Select an image."),
                                                  FileAllowed(["jpg","jpe","png","gif"], 'This file type is not allowerd.')])
    submit = SubmitField('Upload')
    
    
    
class AccountUpdateForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[DataRequired(message="This field cannot be empty."),
                                       Length(min=3, max=15, message="This field's length is from 3 to 15 characters.")])
    email = StringField(label="email",
                           validators=[DataRequired(message="This field cannot be empty."), 
                                       Email(message="Please insert a valid email.")])
    user = {}
    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
        print(self.user)
        if username.data != self.user['username']:
            user_exists = db.user.find_one({"username": re.compile(f'^{username.data}$', re.IGNORECASE)})
            if user_exists:
                raise ValidationError('This username is already in use!')

    def validate_email(self, email):
        print(self.user)
        if email.data != self.user['email']:
            email_exists = db.user.find_one({"email": re.compile(f'^{email.data}$', re.IGNORECASE)})
            if email_exists:
                raise ValidationError('This email is already in use!')