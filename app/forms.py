from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[Length(max=120)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    college_name = StringField('College Name', validators=[Length(max=120)])
    department = StringField('Department', validators=[Length(max=120)])
    skills = StringField('Skills', validators=[Length(max=256)])
    github_link = StringField('GitHub Link', validators=[Length(max=120)])
    linkedin_link = StringField('LinkedIn Link', validators=[Length(max=120)])
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    content = TextAreaField('Say something', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommunityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Community')

    def validate_name(self, name):
        from app.models import Community
        community = Community.query.filter_by(name=name.data).first()
        if community is not None:
            raise ValidationError('Please use a different name.')

class CollaborationRequestForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    skills_required = StringField('Skills Required', validators=[DataRequired(), Length(max=256)])
    team_size = IntegerField('Team Size Required', validators=[DataRequired()])
    submit = SubmitField('Post Request')

class MessageForm(FlaskForm):
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send')
