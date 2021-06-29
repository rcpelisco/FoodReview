from flask import Blueprint, render_template, redirect
from flask import url_for, g, session, request
from food_review import db
from food_review.models import User, LoginCredentials

users = Blueprint('users', __name__)

@users.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        credentials = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        login_credentials = LoginCredentials(db).login(credentials)

        if login_credentials:

            user = User(db).get(login_credentials['user_id'])
            user['login_cred_id'] = login_credentials['id']
            user['user_type_id'] = login_credentials['user_type_id']

            if user:
                session['user'] = user
                g.user = user

    if g.user:
        return redirect(url_for('front_page.index'))
    return render_template('front_page/login.html')
 
@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form['first_name'],
            'middle_name': request.form['middle_name'],
            'last_name': request.form['last_name'],
            'address': request.form['address'],
            'phone_number': request.form['phone_number'],
            'email_address': request.form['email_address'],
        }

        user = User(db, user_data).save()

        login_credentials = {
            'username': request.form['username'],
            'password': request.form['password'],
            'user_id': user['id'],
            'user_type_id': 2,
        }

        LoginCredentials(db, login_credentials).save()

        return redirect(url_for('users.login'))

    return render_template('front_page/register.html')
