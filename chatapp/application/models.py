from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from application import login


class Users(UserMixin,db.Model):
    """Data model for users"""

    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True)
    google_id = db.Column(db.String(50), index=True, nullable=True)
    first_name=db.Column(db.String(50),
                         index=False,
                         nullable=False)
    last_name =db.Column(db.String(50),
                         index=False,
                         nullable=False)
    user_bio = db.Column(db.String (120) , nullable=True)
    email = db.Column (db.String (120) , unique=True , nullable=False)
    image_file = db.Column (db.String (100) , nullable=True , default='default.jpg')
    password = db.Column (db.String (150) , nullable=True)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    chatmaps = db.relationship('Chatmap', backref='author', lazy='dynamic')
    # contacts = db.relationship('Contacts', backref='contact', lazy='dynamic')
    # blocked = db.relationship('Contacts', backref='blocker', lazy='dynamic')

    def __repr__(self):
        return f"User({self.body},{self.chat},{self.author}"

    def set_password (self , password) :
        self.password = generate_password_hash (password)


    def check_password (self , password) :
        return check_password_hash (self.password , password)
        # if password !=self.password:
        #     return False
        # else:
        #     return True

    def to_dict(self):
       """Return object data in easily serializable format"""
       return {
           'name'   : self.first_name,
           'surname': self.last_name,
           'image'  : self.image_file,
       }

@login.user_loader
def load_user (id) :
        return Users.query.get(int (id))


class Messages(db.Model):
    _table_ = 'messages'
    id = db.Column(db.Integer,
                   primary_key=True)
    body=db.Column (db.String (8000) , nullable=False)
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'),nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    attachment = db.Column (db.String (100) , nullable=True )

    def __repr__(self):
        return f"Message({self.body},{self.chat},{self.author}"

    def from_dict(dict):
        return Messages(body=dict['body'],chat = dict['chat'], sender_id = dict['sender_id'])

    def to_dict (self):
        """Return object data in easily serializable format"""
        if self.attachment:
            return {
                'id' : self.id,
               'body' : self.body,
               'date_created': self.date_created,
               'sender_id' : self.sender_id,
                'attachment' : self.attachment,
            }
        else:
            return {
                'id' : self.id ,
                'body' : self.body ,
                'date_created' : self.date_created ,
                'sender_id' : self.sender_id ,
            }


    # followed = db.relationship (
    #     'User' , secondary=followers ,
    #     primaryjoin=(followers.c.follower_id == id) ,
    #     secondaryjoin=(followers.c.followed_id == id) ,
    #     backref=db.backref ('followers' , lazy='dynamic') , lazy='dynamic')

class Chatmap (db.Model) :
    _table_ = 'chat_map'
    id = db.Column (db.Integer ,
                    primary_key=True)
    users = db.Column (db.Integer , db.ForeignKey ('users.id') , nullable=False)
    chats = db.Column (db.Integer , db.ForeignKey ('chat.id') , nullable=False)


    def to_dict (self):
        """Return object data in easily serializable format"""
        return {
           'user': self.author.name,
           'chat': self.chats,
        }
    # def add_users(chat_id):


class Chat(db.Model):
    _table_ = 'chat'
    id = db.Column(db.Integer,
                   primary_key=True)
    name=db.Column (db.String (120) , nullable=True, default = "Chat")
    # chat_messages = db.relationship('Messages', backref='chat', lazy='dynamic')
    chatmap = db.relationship('Chatmap', backref='chat', lazy='dynamic')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict (self):
        """Return object data in easily serializable format"""
        return {
           'name'         : self.name,
           'date created': self.date_created,
        }


