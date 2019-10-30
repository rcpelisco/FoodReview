from flask import Blueprint, render_template, redirect
from flask import url_for, g, session, request
from food_review import db
from food_review.models import User

users = Blueprint('users', __name__)

@users.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@users.route('/account')
def account():
    pass
    # cart = Cart(db).get_user_all_unpaid_items(g.user['id'])
    # bought_items = Cart(db).get_user_all_paid_items(g.user['id'])
    # transaction_history = TransactionHistory(db).get_user_all(g.user['id'])
    
    # if g.user == None:
    #     return redirect(url_for('front_page.index'))
    # return render_template('front_page/users/index.html', 
    #     user=g.user, cart=cart, bought_items=bought_items,
    #     transaction_history=transaction_history)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        credentials = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        user = User(db).login(credentials)
        
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
            'name': request.form['name'],
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password'],
            'is_writer': 0,
        }

        user = User(db, user_data)
        user.save()
        return redirect(url_for('users.login'))

    return render_template('front_page/register.html')
 
# @users.route('/transaction_history', methods=['GET'])
# def transaction_history():
#     history = User(db).get_history(session['user']['id'])
#     return render_template('front_page/register.html',
#         transaction_history=transaction_history,
#         user=session['user'])
