from flask import Blueprint, render_template, request, redirect, url_for, session, g
from food_review import db
from food_review.models import User

users = Blueprint('writers.users', __name__)

@users.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password'],
            'is_writer': 1,
        }

        user = User(db, user_data)
        user.save()
        return redirect(url_for('users.login'))
    return render_template('admin/register.html')        
    
@users.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('front_page.index'))
    