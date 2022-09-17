from app.db import db

store_to_item = db.Table('store_item_tbl',
                        db.Column('store_id', db.Integer, db.ForeignKey('store_tbl.id')),
                        db.Column('item_id', db.Integer, db.ForeignKey('item_tbl.id'))
                        )

class StoreModel(db.Model):
    __tablename__ = 'store_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    location = db.Column(db.String(20), nullable=False)
    items = db.relationship('ItemModel', secondary=store_to_item, backref='stores')
    
    def json(self):
        return {
            'ID': self.id,
            'name': self.name,
            'location': self.location,
            'items': [item.name for item in self.items]
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
