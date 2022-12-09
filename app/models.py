from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# battle = db.Table(
#     'battles',
#     db.Column ('battler_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
#     db.Column ('battled_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
# )

#create models based off our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique = True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    # battles = db.relationship('battles')
    

    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
      
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # def follow(self, user):
    #     self.battled.append(user)
    #     db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(100), nullable=False)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    spec_attack = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __init__(self,title, img_url, hp, attack, defense, spec_attack, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.spec_attack = spec_attack

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_db(self):
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

