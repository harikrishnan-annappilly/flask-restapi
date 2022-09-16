from app.db import db

class StoreModel(db.Model):
    __tablename__ = 'store_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    location = db.Column(db.String(20), nullable=False)
    items = db.relationship('ItemModel', backref='store')
    
    def json(self):
        return {
            'ID': self.id,
            'name': self.name,
            'location': self.location,
            'items': [item.name for item in self.items],
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
