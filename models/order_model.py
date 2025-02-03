from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # This should link to the User table
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.DECIMAL(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'))  # This should link to the Medicines table

    # Relationships
    user = db.relationship('User', backref='orders')
    medicine = db.relationship('Medicine', backref='orders')
