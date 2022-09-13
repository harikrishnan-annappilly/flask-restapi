from app.db import db

class UserModel(db.Model):
    __tablename__ = 'user_tbl'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def json(self):
        return {
            'ID': self.id,
            'username': self.username,
            'password': self.password,
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
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
