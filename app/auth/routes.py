from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import login_user, logout_user, current_user
from app.auth.forms import PokemonChooserForm, UserCreationForm, UserLoginForm
from app.models import User
from werkzeug.security import check_password_hash
import requests
import json
auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(username, email, password)

            user = User(username, email, password)

            # #add user to database heres another idea
            # db.session.add(user)
            # db.session.commit()
            user.save_to_db()
            return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
    

            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password,password):
                    print('Successfully logged in!')
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    print('incorrect password')
            else:
                print('User does not exist.')
    return render_template('login.html', form=form)




@auth.route('/choose', methods=['GET','POST'])
def choose():
    form = PokemonChooserForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemon.data
            print(pokemon)
            print(get_pokemon_stat_data)
    return render_template('choose.html', form=form)




@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
     



#how can i breakdown individual pokemon?

@auth.route('/list', methods=['GET'])
def lst():
    req = requests.get('https://pokeapi.co/api/v2/pokemon')
    data = json.loads(req.content)
    return render_template('list.html', data=data)




# def get_pokemon_stat_data(choice):
#     pokedex = []
#     url = f'https://pokeapi.co/api/v2/pokemon/{choice}'
#     response = requests.get(url)
#     if response.ok:
#         print(f"{choice} has been selected")
#         data = response.json()
#         pokemon =  {
#             'Name': data['forms'][0]['name'],
#             'Ability': data['abilities'][0]['ability']['name'],
#             'Base Experience': data['base_experience'],
#             'Sprite Image URL' : data['sprites']['back_default'], 
#             'Attack Base Stat' : data['stats'][1]['base_stat'],
#             'HP Base Stat' : data['stats'][0]['base_stat'],
#             'Defence Base Stat' : data['stats'][2]['base_stat'],
#         }
#         pokedex.append(pokemon)
#         return(pokedex)

#     else:
#         return'Please choose another pokemon.'
