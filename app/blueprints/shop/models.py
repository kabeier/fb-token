from app import db
from datetime import datetime as dt
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    image = db.Column(db.String)
    category_id = db.Column(db.ForeignKey('category.id'))
    tax = db.Column(db.Float())
    description = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=dt.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product: {self.name} @{self.price}>'

    def from_dict(self, data):
        for field in ['name', 'price', 'image', 'category_id', 'tax', 'description']:
            if field in data:
                if field == 'category_id':
                    _id = Category.query.filter_by(name=data[field]).first().id
                    setattr(self, field, _id)
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'category': Category.query.get(self.category_id).name,
            'tax': self.tax,
            'description': self.description,
            'created_on': self.created_on
        }
        return data

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True)
    products = db.relationship('Product', cascade='all, delete-orphan', backref='category', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Category: {self.name}>'

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'products': [p.to_dict() for p in Product.query.filter_by(category_id=self.id).all()]
        }


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    product_id = db.Column(db.ForeignKey('product.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def from_dict(self, data):
        for field in ['user_id', 'product_id']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        from app.blueprints.authentication.models import User
        return f'{User.query.get(self.user_id).email}: {Product.query.get(self.product_id).name}'