from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '6c88248707fc142f0253bd0b33b84bd7'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'food_review'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

db = MySQL(app)
bcrypt = Bcrypt(app)

from food_review.writers.routes import writers
from food_review.writers.users.routes import users as writers_users
from food_review.writers.recipes.routes import recipes as writers_recipes

from food_review.front_page.routes import front_page
from food_review.front_page.users.routes import users as front_page_users
from food_review.front_page.recipes.routes import recipes as front_page_recipes
from food_review.front_page.recipes.reviews.routes import reviews as front_page_recipes_reviews
from food_review.front_page.recipes.reviews.comments.routes import comments as front_page_recipes_reviews_comments

app.register_blueprint(writers, url_prefix='/writers')
app.register_blueprint(writers_users, url_prefix='/writers')
app.register_blueprint(writers_recipes, url_prefix='/writers/recipes')

app.register_blueprint(front_page, url_prefix='/')
app.register_blueprint(front_page_users, url_prefix='/')
app.register_blueprint(front_page_recipes, url_prefix='/recipes')
app.register_blueprint(front_page_recipes_reviews, url_prefix='/recipes/reviews')
app.register_blueprint(front_page_recipes_reviews_comments, url_prefix='/recipes/reviews/comments')
