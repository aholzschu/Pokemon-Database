from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from app.auth.forms import PokemonChooserForm
from .forms import PostForm
from  app.models import Post
import requests

pokemon = Blueprint('pokemon', __name__, template_folder='pokemon_templates')

# @pokemon.route('/post/create', methods=['GET','POST'])
# def show_menu():
#     user = current_user.id
#     post = PokemonChooserForm.query.get(user)
#     if post:
#         form = PokemonChooserForm()
#         if request.method == 'POST':
#              if form.validate():
#                 pokemon_name= form.pokemon.data
#                 url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
#                 response = requests.get(url)
#                 if response.ok == True:
#                     data=response.json()
#                     post.title = data

#                     post.save_to_db()

#     return render_template('choose.html', form=form)

@pokemon.route('/posts/create', methods =['GET','POST'])
@login_required
def create_post():
    
    form = PostForm()
    if request.method == 'POST':
        img_url = ''
        caption = ''
        if form.validate():
            pokemon_name= form.title.data
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
            response = requests.get(url)
            if response.ok == True:
                    data=response.json()
                    title = data["name"]
                    img_url = data["sprites"]["front_shiny"]
                    caption = data["abilities"][0]["ability"]["name"]
                    # title = form.title.data
                    # img_url = form.img_url.data
                    # caption = form.caption.data

            print(title, img_url, caption)

            post = Post(title, img_url, caption, current_user.id)

            post.save_to_db()

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
                img_url = form.img_url.data
                caption = form.caption.data

                post.title = title
                post.img_url = img_url
                post.caption = caption

                post.update_db()

                return redirect(url_for('pokemon.view_pokemon'))
    else:
        flash('You are not authorized', 'danger')
        return redirect(url_for('pokemon.view_pokemon'))
            
    return render_template('update_posts.html', form = form, post=post)

@pokemon.route('/posts/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        post.delete_from_db()
    return redirect('pokemon.view_pokemon')