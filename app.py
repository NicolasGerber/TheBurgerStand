from flask import Flask
from database import db
from Controller.order_controller import order_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/burguer-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(order_bp, url_prefix='')


if __name__ == '__main__':
    app.run(debug=True)

