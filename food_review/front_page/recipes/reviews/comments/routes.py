from flask import Blueprint, render_template, redirect, url_for, g, session, request
from food_review import db
from food_review.models import Comment

comments = Blueprint('recipes.reviews.comments', __name__)

@comments.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@comments.route('/save', methods=['POST'])
def save():
    comment_data = {
        'content': request.form['content'],
        'review_id': request.form['review_id'],
        'login_cred_id': g.user['login_cred_id']
    }

    comment = Comment(db, comment_data)
    comment = comment.save()

    return redirect(url_for('recipes.view', recipe=request.form['recipe_id']))
 