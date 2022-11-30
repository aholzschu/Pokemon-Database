


from flask import Blueprint, render_template, request
from app.auth.forms import PokemonChooserForm, UserCreationForm

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        
        if form.validate():
            print('post_request_main')
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(username, email, password)
    return render_template('signup.html', form=form)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/choose', methods=['GET','POST'])
def choose():
    form = PokemonChooserForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemon.data
            print(pokemon)
            print(get_pokemon_stat_data)
    return render_template('choose.html', form=form)

#where to input import requests having trouble collecting data using function from previous homework assingment

def get_pokemon_stat_data(choice):
    import requests
    pokedex = []
    url = f'https://pokeapi.co/api/v2/pokemon/{choice}'
    response = requests.get(url)
    if response.ok:
        print(f"{choice} has been selected")
        data = response.json()
        pokemon =  {
            'Name': data['forms'][0]['name'],
            'Ability': data['abilities'][0]['ability']['name'],
            'Base Experience': data['base_experience'],
            'Sprite Image URL' : data['sprites']['back_default'], 
            'Attack Base Stat' : data['stats'][1]['base_stat'],
            'HP Base Stat' : data['stats'][0]['base_stat'],
            'Defence Base Stat' : data['stats'][2]['base_stat'],
        }
        pokedex.append(pokemon)
        return(pokedex)

    else:
        return'Please choose another pokemon.'