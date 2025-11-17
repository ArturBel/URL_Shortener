from .extensions import db
from datetime import datetime


class Urls(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.Text, nullable=False, unique=True)
    count = db.Column(db.Integer, nullable=False, default=0)
    last_access = db.Column(db.DateTime, nullable=False, default=datetime.now())
