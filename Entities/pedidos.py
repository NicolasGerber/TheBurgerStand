from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id=db.Column(db.String(50), primary_key=True)
    cliente = db.Column(db.String(100))
    item = db.Column(db.String(100))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'item': self.item,
            'status': self.status,
            'created_at': self.created_at
        }