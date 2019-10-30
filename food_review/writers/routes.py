from flask import Blueprint, render_template, redirect, url_for
from food_review import db, bcrypt

writers = Blueprint('writers', __name__)

@writers.route('/')
def index():
    pass
    # return redirect(url_for('admin.items.index'))
