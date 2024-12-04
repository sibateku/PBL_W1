from . import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    estimated_budget = db.Column(db.Float, nullable=True)
    actual_spent = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Event {self.title}>"
