from flask import Blueprint, render_template, redirect, url_for, g, session, request
from food_review import db
from food_review.models import Review

reviews = Blueprint('recipes.reviews', __name__)

@reviews.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@reviews.route('/save', methods=['POST'])
def save():
    review_data = {
        'content': request.form['content'],
        'rating': request.form['rating'],
        'recipe_id': request.form['recipe_id'],
        'user_id': g.user['id']
    }

    review = Review(db, review_data)
    review = review.save()

    return redirect(url_for('recipes.view', recipe=review_data['recipe_id']))
 