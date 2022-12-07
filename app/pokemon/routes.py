from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import PostForm
from  app.models import Post
import requests

pokemon = Blueprint('pokemon', __name__, template_folder='pokemon_templates')

@pokemon.route('/posts/create', methods =['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():
            pokemon_name= form.title.data
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
            response = requests.get(url)
            if response.ok == True:
                    data = response.json()
                    title = data["name"]
                    img_url = data["sprites"]["front_shiny"]
                    caption = data['base_experience']
                    hp = data['stats'][0]['base_stat']
                    attack = data['stats'][1]['base_stat']
                    spec_attack = data['stats'][3]['base_stat']
                    defense = data['stats'][2]['base_stat']
                    if title.unique == False:
                        flash(f'Pokemon has already been chosen. Please choose another pokemon', 'danger')
                        return redirect(url_for('pokemon.create_post'))

            else:
                flash(f'Invalid name please choose another pokemon', 'danger')
                return redirect(url_for('pokemon.create_post'))
            



                    # caption = "Base Experience:" + str(base_experience), "Attack Base Stat:" + str(attack), "HP Base Stat:" + str(hp), "Defense Base Stat:" + str(defense)
                    # title = form.title.data
                    # img_url = form.img_url.data
                    # caption = form.caption.data
            
            

            post = Post(title, img_url, caption, hp, attack, defense, spec_attack, current_user.id)
            # if title == post.title():
            #     flash('pokemon has been already been chosen', 'warning')
            #     return redirect(url_for('/posts/create'))
            
            post.save_to_db()
            flash(f'{pokemon_name.title()} has been added to your pokedex', 'success')

            return redirect(url_for('pokemon.view_pokemon'))

        


    return render_template('pokemon.html', form = form)

@pokemon.route('/posts')
def view_pokemon():
    posts = Post.query.all()
    print(posts)
    return  render_template('feed.html', posts=posts[::-1])


@pokemon.route('/posts/<int:post_id>')
def view_single_pokemon(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('single_pokemon.html', post = post)
    else:
        return redirect(url_for('pokemon.view_pokemon'))

@pokemon.route('/posts/update/<int:post_id>', methods = ['GET','POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        if request.method == 'POST':
            if form.validate():
                title = form.title.data
                post.title = title
                post.update_db()

                return redirect(url_for('pokemon.view_pokemon'))
    else:
        flash('You are not authorized', 'danger')
        return redirect(url_for('pokemon.view_pokemon'))
            
    return render_template('update_posts.html', form=form, post=post)

@pokemon.route('/posts/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.delete_from_db()
    flash(f'Deletion successful. Pokedex has been updated', 'danger')    
    return redirect(url_for('pokemon.view_pokemon'))

@pokemon.route('/trainers')
def view_trainers():
    posts = Post.query.all()
    print(posts)
    return  render_template('trainers.html', posts=posts[::-1])





