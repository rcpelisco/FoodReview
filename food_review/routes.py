from flask import Blueprint, render_template
from food_review import db, bcrypt
from food_review.models import User

food_review = Blueprint('food_review', __name__)

@food_review.route('/')
def index():
    return render_template('index.html')

