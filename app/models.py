from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email     = db.Column(db.String(120), unique=True, index=True, nullable=False)
    pw_hash   = db.Column(db.String(256), nullable=False)
    joined_on = db.Column(db.Date, default=date.today)

    def set_password(self, plain):
        self.pw_hash = generate_password_hash(plain)

    def check_password(self, plain) -> bool:
        return check_password_hash(self.pw_hash, plain)


class GuessLog(db.Model):
    __tablename__ = "guess_log"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_name = db.Column(db.String(120), nullable=False)
    school      = db.Column(db.String(120))
    guess       = db.Column(db.String(120))
    is_correct  = db.Column(db.Boolean, default=False)
    used_hint   = db.Column(db.Boolean, default=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="guesses")

class ScoreLog(db.Model):
    __tablename__ = "score_log"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)
    max_points = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='scores')