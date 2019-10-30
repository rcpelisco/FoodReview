from flask import Blueprint, render_template, request, redirect, url_for, session, g
from food_review import db, ROOT_DIR
from food_review.models import User, Recipe
import os
import datetime
import random

recipes = Blueprint('writers.recipes', __name__)

@recipes.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@recipes.route('/create', methods=['GET'])
def create():
    return render_template('front_page/recipes/create.html', user=g.user)
    # item = Item(db).get(item)
    # user = session['user'] if 'user' in session else None
    # return render_template('front_page/recipes/view.html', 
    #     user=user, item=item)

@recipes.route('/save', methods=['POST'])
def save():
    img_path = ''
    image = None

    if('image' in request.files):
        image = request.files['image']
        img_path = image.filename
    
    relative_path = os.path.join('static', 'uploads', 'img')
    path_target = os.path.join(ROOT_DIR, relative_path)

    if img_path != '' and image != None:
        img_path = convert_filename(img_path)
        save_img_path = os.path.join(path_target, img_path)
        image.save(save_img_path)

    recipe_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'img_path': img_path,
        'user_id': g.user['id']
    }

    recipe = Recipe(db, recipe_data)
    recipe = recipe.save()

    return redirect(url_for('recipes.view', recipe=recipe['id']))

def convert_filename(filename):
    random_num = random.randint(0, 501)
    ext = os.path.splitext(filename)[1]
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return "%s-%s%s"%(random_num, date, ext)