from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user,login_required

from . import db
from .models import Chat,Chatmap, Messages, Users, load_user
from .Forms import AddingMessage, NewChat

ChatApi = Blueprint('chat_api', __name__)

        # task = TODOS.from_dict(request.json)
    # except KeyError as e:
    #     return jsonify(f'Missing key: {e.args[0]}'), 400
    #
    # db.session.add(task)
    # db.session.commit()
    # return jsonify(), 200

@ChatApi.route('/chats/<chat_id>', methods = ['DELETE'])
@login_required
def delete(chat_id):
    chat = Chat.query.filter_by(id =chat_id).first()
    chatmap = Chatmap.query.filter_by(chats =chat_id).all()
    for i in chatmap:
        db.session.delete(i)
    messages = Messages.query.filter_by(chat=chat_id).all()
    for message in messages:
        db.session.delete(message)
    db.session.delete (chat)
    db.session.commit()
    if current_user.is_authenticated :
        user_id = current_user.get_id ()
        chats = Chat.query.join(Chatmap , (Chatmap.chats == Chat.id)).filter(Chatmap.users == user_id).all ()
        chat_list = []
        for c in chats :
            chat_list.append (dict (
                info=c ,
                last_message=Messages.query.filter_by (chat=c.id).order_by (Messages.date_created.desc ()).first ()
            ))
    return render_template('chat.html', chats=chat_list, user_id=user_id )


# @ChatApi.route('/<id>', methods=['PUT'])
# def update_task(id):
#
#     try:
#         task = TODOS.query.filter_by(id =id).first()
#         task.description = request.json.get ('description' , task.description)
#         task.due_date= request.json.get ('due_date' , task.due_date)
#         db.session.commit ()
#     except KeyError as e:
#         return jsonify(f'Missing key: {e.args[0]}'), 400
#
#     db.session.commit()
#     return jsonify(), 200

@ChatApi.route('/chats/<chat_id>/messages', methods=['GET', 'POST'])
@login_required
def messages(chat_id):   
    if request.method == 'GET':
        user_id = int(request.args.get('user_id'))
        messages = Messages.query.filter_by (chat=chat_id).all ()
        list_of_messages = ([x.to_dict() for x in messages])
        for mssg in list_of_messages:
            sender=mssg.get("sender_id")
            user=Users.query.filter_by(id=sender).first()
            mssg.update({"sender_name": user.first_name })
        return jsonify(list_of_messages) , 200

    if request.method == 'POST':
        try:
            print(request.json)
            message = Messages.from_dict (request.json)
        except KeyError as e:
            return jsonify(f'Missing key: {e.args[0]}'), 400

        db.session.add(message)
        db.session.commit()
        message = message.to_dict()
        return jsonify(message) , 200
        # form = AddingMessage ()
        # if form.validate_on_submit () :
        #     message = Messages (body=form.body.data )
        #     db.session.add (message)
        #     db.session.commit ()
        # return render_template ('adding_message.html' , form=form)


@ChatApi.route('/chats', methods = ['GET'])
@login_required
def chat_list():
        if current_user.is_authenticated:
            user_id = current_user.get_id()
            # user_id = load_user(user_id)
        else: 
            user_id = int (request.args.get ('user_id'))
        # user = Users.get(user_id)
        # user_name = f"{user.first_name} "
        # # chats = Chat.query.filter(Chat.creator_id == user_id).all()
        chats = Chat.query.join(Chatmap, (Chatmap.chats==Chat.id)).filter(Chatmap.users == user_id).all ()
        chat_list=[]
        for c in chats:
            chat_list.append(dict(
                info=c,
                last_message=Messages.query.filter_by(chat=c.id).order_by(Messages.date_created.desc()).first()
            ))
        image_file = url_for('static', filename='images/profilep/'+ current_user.image_file)
        return render_template('chat.html', chats=chat_list, user_id=user_id, image_file=image_file )

@ChatApi.route('/chats/new', methods = ['GET','POST'])
@login_required
def new_chat():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        form = NewChat()
        if form.validate_on_submit():
            new_chat = Chat(name=form.name.data,creator_id = user_id)
            # new_chat = Chat(name=chat['name'],creator_id=user_id)
            # email=form.email.data
            db.session.add(new_chat)
            db.session.commit()
            new_chatmap1 = Chatmap(users=user_id, chats=new_chat.id)
            contact=Users.query.filter_by(email=form.email.data).first()
            print('contact.id')
            contact_id=contact.id
            new_chatmap2 = Chatmap(users=contact_id,chats=new_chat.id)
            db.session.add(new_chatmap1)
            db.session.add(new_chatmap2)
            db.session.commit()
            return redirect(url_for('chat_api.chat_list'))

        return render_template('createchat.html',form=form)
    else:
        flash('You need to log in!')
        return redirect(url_for('login'))


@ChatApi.route('/chats/<chat_id>', methods = ['POST'])
@login_required
def add_user(chat_id):
    #needs to be added to the function on top
    user_email = request.args.get ('user')
    user = Users.query.filter_by(email = user_email).first()
    chatmap = Chatmap.query.filter(users = user.id,chats = chat_id ).first()
    if chatmap:
        pass
    else:
        new_chatmap = Chatmap(users = user.id, chats = chat_id)
        db.session.add(new_chatmap)
        db.session.commit()
    chatmaps = Chatmap.query.filter_by(chats = chat_id).all()
    list_chatmap = ([c.to_dict() for c in chatmaps ])
    return jsonify(list_chatmap) , 200

@ChatApi.route('/chats/<chat_id>/users', methods=['GET'])
# @login_required
def show_users(chat_id):
    chatmaps = Chatmap.query.filter_by(chats = chat_id).all()
    list_chatmap = ([c.author.to_dict() for c in chatmaps])
    return jsonify(list_chatmap) , 200






