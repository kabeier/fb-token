from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField

class ProfileForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    email = StringField(validators=[Email()])
    password = PasswordField()
    confirm_password = PasswordField(validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')

class EditBlogPostForm(FlaskForm):
    body = StringField()
    submit = SubmitField('Edit Post')