from flask import Flask

from Entities.pedidos import OrderStatus
from Services.order_service import get_locked_orders, repo
from database import db
from Controller.order_controller import order_bp
from worker import start_worker
from rescue_task import rescue_and_enqueue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/burguer-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(order_bp, url_prefix='')

@app.cli.command("start-consumer")
def start_consumer():
    with app.app_context():
        start_worker()

@app.cli.command("rescue-orders")
def rescue_orders():
    target_status = [
        OrderStatus.RECEBIDO.value,
        OrderStatus.PREPARACAO.value,
        'Pendente',
        'Pendende_Pagamento'
    ]
    orders_list = repo.get_orders_locked_repo(status_list=target_status)
    with app.app_context():
        rescue_and_enqueue(orders_list)

if __name__ == '__main__':


    app.run(debug=True)

