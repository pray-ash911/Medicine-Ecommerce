# models/wishlist_model.py
from app import db


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'))

    user = db.relationship('User', backref='wishlist')
    medicine = db.relationship('Medicine', backref='wishlisted_by')
