from flask import request
from Services.order_service import create_order, get_order, get_all_orders
from flask import Blueprint

order_bp = Blueprint('order_controller', __name__)

@order_bp.route('/order', methods=['POST'])
def CreateOrder():

    OrderInfo = request.get_json(force=True)
    order_obj = create_order(OrderInfo)
    response = {"id": order_obj.id,
            "status": order_obj.status,
            "Message": "Pedido colocado na fila"
            }
    return response, 200


@order_bp.route('/order/<string:order_id>', methods=['GET'])
def get_order_from_services(order_id):
    return get_order(order_id), 200

@order_bp.route('/order', methods=['GET'])
def get_all():
    return get_all_orders(), 200