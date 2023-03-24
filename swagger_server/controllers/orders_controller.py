import connexion
import six
from sqlalchemy import exc
from database.database import db
from database.dbmodels.order_dbmodel import OrderDbModel
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.models.order import Order  # noqa: E501
from swagger_server import util


def create_order(body):  # noqa: E501
    """Creates new order

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Order
    """
    if connexion.request.is_json:
        try:
            body = Order.from_dict(connexion.request.get_json())  # noqa: E501
            order_db = body.toOrderDbModel()
            is_order_existed = db.session.query(OrderDbModel).filter_by(customer_id=order_db.customer_id,
                                                                        baker_id=order_db.baker_id,
                                                                        start_date=order_db.start_date).first()
            if is_order_existed:
                return 'such order is already exist', 400
            else:
                db.session.add(order_db)
                db.session.commit()
                resp_db = db.session.query(OrderDbModel).filter_by(customer_id=order_db.customer_id,
                                                                   baker_id=order_db.baker_id,
                                                                   start_date=order_db.start_date).first()
                resp = Order()
                resp.fromOrderDbModel(resp_db)
                return resp, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400


def get_order_by_id(order_id):  # noqa: E501
    """Returns order with requested ID

     # noqa: E501

    :param order_id: Order&#x27;s ID
    :type order_id: str

    :rtype: Order
    """
    try:
        order_db = db.session.query(OrderDbModel).filter_by(id=order_id).first()
        print(order_db)
        if order_db:
            resp = Order()
            resp.fromOrderDbModel(order_db)
            return resp, 200
        else:
            return 'no customer found for that id', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_orders(status=None, customer_id=None, baker_id=None):  # noqa: E501
    """Returns orders

     # noqa: E501

    :param status: 
    :type status: str
    :param customer_id: 
    :type customer_id: str
    :param baker_id: 
    :type baker_id: str

    :rtype: List[Order]
    """
    print(f'{status=}, {customer_id=}, {baker_id=}')
    orders_db = []
    try:
        match bool(status), bool(customer_id), bool(baker_id):
            case True, False, False:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.status == status)
            case True, True, False:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.status == status,
                                                                  OrderDbModel.customer_id == customer_id)
            case True, False, True:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.status == status,
                                                                  OrderDbModel.baker_id == baker_id)
            case False, True, False:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.customer_id == customer_id)

            case False, False, True:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.baker_id == baker_id)
            case True, True, True:
                orders_db = db.session.query(OrderDbModel).filter(OrderDbModel.status == status,
                                                                  OrderDbModel.customer_id == customer_id,
                                                                  OrderDbModel.baker_id == baker_id)
            case False, False, False:
                orders_db = db.session.query(OrderDbModel).all()
        print(f'{orders_db=}')
        if orders_db:
            resp = []
            for order_db in orders_db:
                order = Order()
                order.fromOrderDbModel(order_db)
                print(f'{order=}')
                resp.append(order)
            return resp, 200
        else:
            return [], 200  # TODO maybe it should be 404 error

    except exc.SQLAlchemyError:
        return 'server error', 500


def update_order_by_id(body, order_id):  # noqa: E501
    """Updates existing order

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param order_id: Order&#x27;s ID
    :type order_id: str

    :rtype: Order
    """
    if connexion.request.is_json:
        body = Order.from_dict(connexion.request.get_json())  # noqa: E501
        order_db = db.session.query(OrderDbModel).filter_by(id=order_id).first()
        if order_db:
            updated_order_db = body.toOrderDbModel()
            order_db.baker_id = updated_order_db.baker_id
            order_db.customer_id = updated_order_db.customer_id
            order_db.status = updated_order_db.status
            order_db.price = updated_order_db.price
            order_db.products = updated_order_db.products
            order_db.start_date = updated_order_db.start_date
            db.session.commit()
            resp_db = db.session.query(OrderDbModel).filter_by(id=order_id).first()
            resp = Order()
            resp.fromOrderDbModel(resp_db)
            return resp, 200
        else:
            return 'no such order found', 404
    else:
        return 'bad request', 400
