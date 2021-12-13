from flask_login.utils import login_required
from store import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from store.models import Orders, User
from store.forms import RegisterForm, LoginForm
from store import db
from flask_login import login_user, logout_user
from flask import json
from flask import jsonify, make_response, request, session
from flask_session import Session

@app.route('/')
@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                         email=form.email.data,
                         password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('account'))
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
            session["user_id"] = attempted_user.id 
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('account'))
        else:
            flash('Wrong usermane or password', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')

    return redirect(url_for("home_page"))

@app.route('/account')
@login_required
def account():
    pass

    return render_template('account.html')


@app.route('/products', methods=['GET', 'POST'])
@login_required
def product_page():
    if request.method == "POST":
        try:
            new_entry = Orders(door_finish = request.json['door_finish'], door_glass  = request.json['glass'], door_width = request.json['door_width'], door_height  = request.json['door_height'], user_id = session["user_id"])
            db.session.add(new_entry)
            db.session.commit()
            # flash(f"Thanks for your request! We'll reply to you shortly.", category='success')
            # return redirect(url_for("account")) 

        except:
            db.session.rollback()
            print("An error")
        

    
    return render_template('products.html')



@app.route('/contact')
def contact_page():
    return render_template('contact.html')
