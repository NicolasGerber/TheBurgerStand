from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def salvar_pedido(NewOrder):
    try:
        db.session.add(NewOrder)
        db.session.commit()
        return jsonify(NewOrder.to_dict(),), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500
