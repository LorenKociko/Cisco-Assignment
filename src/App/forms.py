from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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