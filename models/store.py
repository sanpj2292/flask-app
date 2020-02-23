from db import db


class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Back Reference
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

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
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def castToItems(cls, rows):
        items = []
        for row in rows:
            item = cls(*row)
            items.append(item.json())
        return items
