from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_manager, login_user, logout_user
from .models import Users

from .chat import ChatApi
from .Forms import LoginForm, RegistrationForm
from . import db

app.register_blueprint(ChatApi, url_prefix='/api')

# homepage
@app.route('/', methods=['GET'])
def index():
    # user_id = int (request.args.get ('user_id'))
    # user = Users.query.filter_by(id=user_id).first()
    return render_template('hello.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(first_name=form.first_name.data,last_name = form.last_name.data, email=form.email.data, password = form.password.data)
        # user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)