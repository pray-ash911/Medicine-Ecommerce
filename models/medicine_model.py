# models/medicine_model.py
from app import db

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    discount = db.Column(db.Float, nullable=True, default=0.0)  # Discount field

    def get_discounted_price(self):
        """Calculate price after discount."""
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price
