from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_manager, login_user
from .models import Users

from .chat import ChatApi
from .Forms import LoginForm

app.register_blueprint(ChatApi, url_prefix='/api')

# homepage
@app.route('/', methods=['GET'])
def index():
    user_id = int (request.args.get ('user_id'))
    user = Users.query.filter_by(id=user_id).first()
    return render_template('hello.html', user = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)