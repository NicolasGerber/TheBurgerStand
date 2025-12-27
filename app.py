from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)


cardapio = [
    {"id":1, "nome":"X-BACON", "preco": 22.00 },
    {"id":2, "nome":"X-SALADA", "preco": 20.00 },
    {"id":3, "nome":"X-TUDO", "preco": 30.00 }
]

@app.route('/hello')
def hello():
    return 'Hello World!'
@app.route('/all_orders', methods=['GET'])
def all_orders():
    return jsonify(cardapio), 200
@app.route('/orders/<string:id>', methods=['GET'])
def getlanches(id):
    for lanche in cardapio:
        if lanche['id'] == id:
            return lanche

    return "Lanche não encontrado", 404

@app.route('/order', methods=['POST'])
def CreateOrder():
    OrderInfo = request.get_json(force=True)

    NewOrder ={
        "id":uuid4(),
        "name":OrderInfo["name"],
        "price":OrderInfo["price"]
    }
    print(NewOrder)
    cardapio.append(NewOrder), 201

    return  jsonify(NewOrder), 201
if __name__ == '__main__':
    app.run(debug=True)

