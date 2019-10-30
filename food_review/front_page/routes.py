from flask import Blueprint, render_template, redirect, url_for, session
from food_review import db
from food_review.models import Recipe

front_page = Blueprint('front_page', __name__)

@front_page.route('/')
def index():
    recipes = Recipe(db).all()
    user = session['user'] if 'user' in session else None
    return render_template('front_page/index.html', user=user, recipes=recipes)
