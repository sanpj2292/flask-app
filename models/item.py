from db import db


class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))
    # Foreign Key
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, _id, name, price, store_id):
        self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def castToItems(cls, rows):
        items = []
        for row in rows:
            item = cls(*row)
            items.append(item.json())
        return items
