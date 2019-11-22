import os
import secrets
from PIL import Image
from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_manager, login_user, logout_user, login_required
from .models import Users

from .chat import ChatApi
from .Forms import LoginForm, RegistrationForm, UpdateForm
from . import db

app.register_blueprint(ChatApi, url_prefix='/api')

# homepage
@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
         user_id = current_user.get_id()
         user = Users.query.get(user_id)
         user_name = user.first_name
    else: user_name = ""
    # user_id = int (request.args.get ('user_id'))
    # user = Users.query.filter_by(id=user_id).first()
    return render_template('hello.html', name = user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat_api.chat_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        next_page=request.args.get('next')
        login_user(user, remember=form.remember_me.data)
        return redirect(next_page) if next_page else redirect(url_for('chat_api.chat_list'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat_api.chat_list'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(first_name=form.first_name.data,last_name = form.last_name.data, email=form.email.data, password = form.password.data)
        # user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


def save_picture(user_image):
    file_name = secrets.token_hex(8)
    _ , f_ext = os.path.splitext (user_image.filename)
    picture_fn = file_name + f_ext
    picture_path = os.path.join (app.root_path , 'static/images/profilep' , picture_fn)
    # user_image.save(picture_path)

    output_size = (125, 125)
    i = Image.open(user_image)
    i.thumbnail (output_size)
    i.save (picture_path)

    return picture_fn

def delete_image(image_name):
    picture_path = os.path.join(app.root_path,'static/images/profilep' , image_name )
    os.remove(picture_path)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def update():
        form = UpdateForm()
        if form.validate_on_submit():
            if form.picture.data:
                form_picture = save_picture(form.picture.data)
                current_image = current_user.image_file
                current_user.image_file = form_picture
                delete_image(current_image)
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.user_bio = form.user_bio.data
            db.session.commit()
            flash("Your account has been updated!", "success")
            return redirect(url_for('update'))
        elif request.method == "GET":
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.user_bio.data = current_user.user_bio
            form.email.data = current_user.email
        user_image = url_for('static', filename='images/profilep/'+ current_user.image_file)
        return render_template('account.html', form=form, image_file = user_image)