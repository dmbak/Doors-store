from store import db, login_manager
from store import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=40), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)


    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)



class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    door_finish = db.Column(db.String(length=20), nullable=False)
    door_glass = db.Column(db.String(length=20), nullable=False)
    door_width = db.Column(db.String(length=20), nullable=False)
    door_height = db.Column(db.String(length=20), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Orders {self.name}'
