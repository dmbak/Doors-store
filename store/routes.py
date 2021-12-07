from store import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from store.models import Orders, User
from store.forms import RegisterForm, LoginForm
from store import db
from flask_login import login_user, logout_user
from flask import json
from flask import jsonify, make_response, request

@app.route('/')
@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/products')
def product_page():
   
    return render_template('products.html')

@app.route('/processOrderInfo', methods=['GET', 'POST'])
def processOrderInfo():
    # orderInfo = request.get_json()
    # door_finish = orderInfo['door_finish']
    # glass = orderInfo['glass']
    door_finish = request.json['door_finish']
    glass = request.json['glass']

    return '''
           The Door Finish value is: {}
           The Glass value is: {}'''.format(door_finish, glass)


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                         email=form.email.data,
                         password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('product_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('product_page'))
        else:
            flash('Wrong usermane or password', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')

    return redirect(url_for("home_page"))
