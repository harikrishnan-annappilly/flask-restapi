from app.db import db

class ItemModel(db.Model):
    __tablename__ = 'item_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    price = db.Column(db.Float(precision=3), nullable=False)
    
    def json(self):
        return {
            'ID': self.id,
            'name': self.name,
            'price': self.price,
            'stores': [store.name for store in self.stores]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
