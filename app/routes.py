from app import app
from flask import render_template
from.models import User

# from app.forms import UserCreationForm

@app.route('/')
@app.route('/home')
def home():
    users = User.query.all()
    return render_template('index.html', users = users)
#form=form


