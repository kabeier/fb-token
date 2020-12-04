from app import db
from datetime import datetime as dt


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'))

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<BlogPost: {self.id} | {self.body[:10]}...>'

    def from_dict(self, data):
        from app.blueprints.authentication.models import User

        for field in ['body', 'user_id']:
            if field in data:
                if field == 'user_id':
                    if isinstance(field, str):
                        _id = User.query.filter_by(email=data[field]).first().id
                        setattr(self, field, _id)
                    else:
                        raise ValueError
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        from app.blueprints.authentication.models import User

        data = {
            'id': self.id,
            'body': self.body,
            'created_on': self.created_on,
            'user_id': User.query.get(self.user_id).email 
        }
        return data