from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from Services.order_service import create_order
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/burguer-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/order', methods=['POST'])
def CreateOrder():

    OrderInfo = request.get_json(force=True)
    create_order(OrderInfo)
    return {'message': 'Order Created'}, 201
@app.route('/hello')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)

