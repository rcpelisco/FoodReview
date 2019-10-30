from flask import Blueprint, render_template, redirect, url_for, g, session, request
from food_review import db
from food_review.models import Recipe

recipes = Blueprint('recipes', __name__)

@recipes.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@recipes.route('/view/<recipe>', methods=['GET'])
def view(recipe):
    recipe = Recipe(db).get(recipe)
    user = session['user'] if 'user' in session else None
    return render_template('front_page/recipes/view.html', 
        user=user, recipe=recipe)

@recipes.route('/delete/<item>', methods=['GET'])
def delete(item):
    return ''
    # Cart(db).delete(item)
    # return redirect(url_for('users.account'))
 
@recipes.route('/add_to_cart/<item>', methods=['GET', 'POST'])
def add_to_cart(item):
    return ''
    # item = Item(db).add_to_cart(item, session['user']['id'])
    # return redirect(url_for('users.account'))