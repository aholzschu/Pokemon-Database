from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    # img_url = StringField('Image URL', validators=[DataRequired()])
    # caption = StringField('Caption', validators=[DataRequired()])
    submit = SubmitField()