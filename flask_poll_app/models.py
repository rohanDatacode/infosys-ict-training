from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)

