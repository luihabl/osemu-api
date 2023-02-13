from ..extensions import db

class Console(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))