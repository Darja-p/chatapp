from flask import Blueprint, jsonify, request, render_template

from . import db
from .models import Chat,Chatmap, Messages
from .Forms import AddingMessage

ChatApi = Blueprint('chat_api', __name__)



        # task = TODOS.from_dict(request.json)
    # except KeyError as e:
    #     return jsonify(f'Missing key: {e.args[0]}'), 400
    #
    # db.session.add(task)
    # db.session.commit()
    # return jsonify(), 200






# @ChatApi.route('/<id>', methods = ['DELETE'])
# def delete(id):
#     task = TODOS.query.filter(TODOS.id == id).first()  #order_by(TODOS.due_date).
#     db.session.delete (task)
#     db.session.commit ()
#     return jsonify () , 200


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
def messages(chat_id):
    user_id = int(request.args.get('user_id'))

    if request.method == 'GET':
        chats = Chatmap.query.filter (Chatmap.users == user_id, Chatmap.chats == chat_id).all ()
        if chats is None:
            return "this user is not a participant in specified chat"
        else:
            messages = Messages.query.filter_by (chat=chat_id).all ()
            return jsonify ([x.to_dict() for x in messages]) , 200

    if request.method == 'POST':
        try:
            message = Messages.from_dict (request.json)
        except KeyError as e:
            return jsonify(f'Missing key: {e.args[0]}'), 400

        db.session.add(message)
        db.session.commit()
        return jsonify(), 200
        # form = AddingMessage ()
        # if form.validate_on_submit () :
        #     message = Messages (body=form.body.data )
        #     db.session.add (message)
        #     db.session.commit ()
        # return render_template ('adding_message.html' , form=form)


@ChatApi.route('/chats', methods = ['GET'])
def chat_list():
    user_id = int (request.args.get ('user_id'))
    # chats = Chat.query.filter(Chat.creator_id == user_id).all()
    chats = Chat.query.join(Chatmap, (Chatmap.chats==Chat.id)).filter(Chatmap.users == user_id).all ()
    return jsonify([x.to_dict() for x in chats]), 200


