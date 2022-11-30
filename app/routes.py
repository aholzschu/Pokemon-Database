from app import app
from flask import render_template

from app.forms import UserCreationForm

@app.route('/')
@app.route('/home')
def home():
    form = UserCreationForm()
    return render_template('index.html', form=form)



