import bcrypt
from datetime import datetime

from app import db


class TimestampMixin(object):
    createdAt = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class MyUser(TimestampMixin, db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    bio = db.Column(db.Text)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password)
