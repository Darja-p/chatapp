import os
import json
import secrets
import requests
from PIL import Image
from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_manager, login_user, logout_user, login_required
from .models import Users

from .chat import ChatApi
from .Forms import LoginForm, RegistrationForm, UpdateForm
from . import db
from . import oauth_client

app.register_blueprint(ChatApi, url_prefix='/api')

# function for retrieving Google’s provider configuration
def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()

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

# login page using Google OAuth
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat_api.chat_list'))

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg ()
    authorization_endpoint = google_provider_cfg ["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = oauth_client.prepare_request_uri (
        authorization_endpoint ,
        redirect_uri=request.base_url + "/callback" ,
        scope=["openid" , "email" , "profile"] ,
    )

    return redirect (request_uri)
    """form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            next_page=request.args.get('next')
            login_user(user, remember=form.remember_me.data)
            return redirect(next_page) if next_page else redirect(url_for('chat_api.chat_list'))
        return render_template('login.html', form=form)"""

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg ["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url , headers , body = oauth_client.prepare_token_request (
        token_endpoint ,
        authorization_response=request.url ,
        redirect_url=request.base_url ,
        code=code
    )
    token_response = requests.post (
        token_url ,
        headers=headers ,
        data=body ,
        auth=(app.config['GOOGLE_CLIENT_ID'] ,app.config['GOOGLE_CLIENT_SECRET']) ,
    )

    # Parse the tokens
    oauth_client.parse_request_body_response (json.dumps (token_response.json ()))

    # find and hit the URL
    # from Google that gives the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg ["userinfo_endpoint"]
    uri , headers , body = oauth_client.add_token (userinfo_endpoint)
    userinfo_response = requests.get (uri , headers=headers , data=body)

    # Verification of user's email.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json ().get ("email_verified") :
        unique_id = userinfo_response.json () ["sub"]
        users_email = userinfo_response.json () ["email"]
        picture = userinfo_response.json () ["picture"]
        users_name = userinfo_response.json () ["given_name"]
    else :
        return "User email not available or not verified by Google." , 400

    # Create a user in db with the information provided
    # by Google
    user = Users (
        id_=unique_id , first_name=users_name ,  email=users_email , image_file=picture)

    # Doesn't exist? Add it to the database.
    if not Users.get (unique_id) :
        db.session.add (user)
        db.session.commit ()

    # Begin user session by logging the user in
    login_user (user)

    # Send user to chats
    return redirect(url_for('chat_api.chat_list'))

@app.route('/logout')
@login_required
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
        user.set_password(form.password.data)
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