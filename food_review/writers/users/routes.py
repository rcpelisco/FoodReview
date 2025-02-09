from flask import Blueprint, render_template, request, redirect, url_for, session, g
from food_review import db
from food_review.models import User, LoginCredentials

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
            'first_name': request.form['first_name'],
            'middle_name': request.form['middle_name'],
            'last_name': request.form['last_name'],
            'address': request.form['address'],
            'email_address': request.form['email_address'],
            'phone_number': request.form['phone_number'],
        }

        user = User(db, user_data).save()

        login_credentials = {
            'username': request.form['username'],
            'password': request.form['password'],
            'user_id': user['id'],
            'user_type_id': 1,
        }

        LoginCredentials(db, login_credentials).save()

        return redirect(url_for('users.login'))
    return render_template('writers/register.html')  
    
@users.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('front_page.index'))
    