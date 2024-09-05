from datetime import datetime, timezone
from .exts import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    # Define a unique backref name for messages
    messages_sent = db.relationship('Messages', backref='sender', lazy=True)

    def __repr__(self):
        return f"<User {self.userName}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rooms', lazy=True))

    def __repr__(self):
        return f"<Room {self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title):
        self.title = title
        db.session.commit()


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('messages_received', lazy=True))
    room = db.relationship('Room', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f"<Message {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, text):
        self.text = text
        db.session.commit()
