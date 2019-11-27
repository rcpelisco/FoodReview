from flask import Blueprint, render_template, request, redirect, url_for, session, g
from food_review import db, ROOT_DIR
from food_review.models import User, Recipe, Ingredient, RecipeIngredient
import os, datetime, random, json

recipes = Blueprint('writers.recipes', __name__)

@recipes.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@recipes.route('/create', methods=['GET'])
def create():
    return render_template('front_page/recipes/create.html', user=g.user)

@recipes.route('/save', methods=['POST'])
def save():
    img_path = ''
    image = None

    if('image' in request.files):
        image = request.files['image']
        img_path = image.filename
    
    relative_path = os.path.join('static', 'uploads', 'img')
    path_target = os.path.join(ROOT_DIR, relative_path)
    
    if not os.path.exists(path_target):
        os.makedirs(path_target)

    if img_path != '' and image != None:
        img_path = convert_filename(img_path)
        save_img_path = os.path.join(path_target, img_path)
        image.save(save_img_path)

    recipe_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'img_path': img_path,
        'login_cred_id': g.user['login_cred_id']
    }

    recipe = Recipe(db, recipe_data)
    recipe = recipe.save()


    for ingredient in json.loads(request.form['ingredient']):
        i = Ingredient(db, ingredient).save()
        
        recipe_ingredient = {
            'recipe_id': recipe['id'],
            'ingredient_id': i['id']
        }

        ri = RecipeIngredient(db, recipe_ingredient).save()
        

    return redirect(url_for('recipes.view', recipe=recipe['id']))

def convert_filename(filename):
    random_num = random.randint(0, 501)
    ext = os.path.splitext(filename)[1]
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return "%s-%s%s"%(random_num, date, ext)