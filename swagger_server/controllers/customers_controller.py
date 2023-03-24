import connexion
import six
from sqlalchemy import exc
from database.database import isContactExisted, db
from database.dbmodels.customer_dbmodel import CustomerDbModel
from database.dbmodels.customer_review_dbmodel import CustomerReviewDbModel
from swagger_server.models.customer import Customer  # noqa: E501
from swagger_server.models.customer_review import CustomerReview  # noqa: E501
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server import util


def create_customer(body):  # noqa: E501
    """Creates new customer

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Customer
    """
    if connexion.request.is_json:
        body = Customer.from_dict(connexion.request.get_json())  # noqa: E501
        print(f'request body ={body}')
        new_customer = body.toCustomerDbModel()
        new_customer.rating_points = 0
        new_customer.reviews_quantity = 0
        new_customer.rating = 0
        print(f'new_customer_db = {new_customer}')
        contact = new_customer.contact
        if isContactExisted(CustomerDbModel, contact):
            return 'bad request: this contact is already been used', 400
        else:
            try:
                db.session.add(new_customer)
                db.session.commit()
                resp_db = db.session.query(CustomerDbModel).filter_by(contact=contact, name=new_customer.name).first()
                resp = Customer()
                resp.fromCustomerDbModel(resp_db)
                return resp, 200
            except exc.SQLAlchemyError:
                db.session.rollback()
                return 'server error', 500
    else:
        return 'bad request', 400


def create_customer_review(body, customer_id):  # noqa: E501
    """Creates customer review

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param customer_id: Customer&#x27;s ID
    :type customer_id: str

    :rtype: CustomerReview
    """
    if connexion.request.is_json:
        body = CustomerReview.from_dict(connexion.request.get_json())  # noqa: E501
        customer_review_dbmodel = body.toCustomerReviewDbModel()
        customer_review_dbmodel.customer_id = customer_id
        try:
            author_id = customer_review_dbmodel.author_id
            is_customer_existed = bool(db.session.query(CustomerDbModel).filter_by(id=customer_id).first())
            print(f'{is_customer_existed=}')
            if not is_customer_existed:
                return 'bad request: no customer with that id', 400
            else:
                review_db = db.session.query(CustomerReviewDbModel).filter_by(author_id=author_id,
                                                                              customer_id=customer_id).first()
                print(f'review_db = {review_db}')
                if review_db:
                    prev_rating = review_db.rating
                    resp_db = db.session.query(CustomerReviewDbModel).filter_by(author_id=author_id).first()
                    resp_db.rating = customer_review_dbmodel.rating
                    resp_db.description = customer_review_dbmodel.description
                    db.session.commit()
                    print(f'>>>resp_db = {resp_db}')
                    print(f'>>>>prev rating = {prev_rating}')
                    resp = CustomerReview()
                    resp.fromCustomerReviewDbModel(resp_db)
                    customer_db = db.session.query(CustomerDbModel).filter_by(id=customer_id).first()
                    customer_db.rating_points -= prev_rating
                    customer_db.rating_points += customer_review_dbmodel.rating
                    customer_db.updateRating()
                    db.session.commit()
                    return resp, 200
                else:
                    db.session.add(customer_review_dbmodel)
                    db.session.commit()
                    resp_db = db.session.query(CustomerReviewDbModel).filter_by(author_id=author_id).first()
                    resp = CustomerReview()
                    resp.fromCustomerReviewDbModel(resp_db)
                    customer_db = db.session.query(CustomerDbModel).filter_by(id=customer_id).first()
                    print(customer_db)
                    customer_db.rating_points += customer_review_dbmodel.rating
                    customer_db.reviews_quantity += 1
                    customer_db.updateRating()
                    db.session.commit()
                    print(customer_db)

                    return resp, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400


def delete_customer_review_by_id(customer_id, review_id):  # noqa: E501
    """Deletes customer review

     # noqa: E501

    :param customer_id: Customer&#x27;s ID
    :type customer_id: str
    :param review_id: Review&#x27;s ID
    :type review_id: str

    :rtype: None
    """
    print(f'{customer_id=} \n {review_id=}')
    review_db = db.session.query(CustomerReviewDbModel).filter_by(customer_id=customer_id, id=review_id).first()
    prev_rating = review_db.rating
    print(f'{review_db=}')
    if review_db:
        try:
            db.session.delete(review_db)
            customer_db = db.session.query(CustomerDbModel).filter_by(id=customer_id).first()
            customer_db.rating_points -= prev_rating
            customer_db.reviews_quantity -= 1
            customer_db.updateRating()
            db.session.commit()
            return {}, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    return 'no review found', 404


def get_customer_by_id(customer_id):  # noqa: E501
    """Returns customer with requested Id

     # noqa: E501

    :param customer_id: Customer&#x27;s ID
    :type customer_id: str

    :rtype: Customer
    """
    try:
        customer_db = db.session.query(CustomerDbModel).filter_by(id=customer_id).first()
        print(customer_db)
        if customer_db:
            resp = Customer()
            resp.fromCustomerDbModel(customer_db)
            return resp, 200
        else:
            return 'no customer found for that id', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_customer_reviews_by_customer_id(customer_id):  # noqa: E501
    """Returns customer reviews

     # noqa: E501

    :param customer_id: Customer&#x27;s ID
    :type customer_id: str

    :rtype: List[CustomerReview]
    """
    try:
        reviews_db = db.session.query(CustomerReviewDbModel).filter_by(customer_id=customer_id).all()
        print(reviews_db)
        if reviews_db:
            response = []
            for review in reviews_db:
                resp = CustomerReview()
                resp.fromCustomerReviewDbModel(review)
                response.append(resp)
            return response, 200
        else:
            return 'no reviews found for that customer', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_customers(status=None, rating=None):  # noqa: E501
    """Returns customers

     # noqa: E501

    :param status: 
    :type status: str
    :param rating:
    :type rating: float

    :rtype: List[Customer]
    """
    try:
        print(f'{status=}, {rating=}')
        customers_db = []
        match bool(status), bool(rating):
            case True, False:
                customers_db = db.session.query(CustomerDbModel).filter(CustomerDbModel.status == status)
            case False, True:
                customers_db = db.session.query(CustomerDbModel).filter(CustomerDbModel.rating >= rating)
            case True, True:
                customers_db = db.session.query(CustomerDbModel).filter(CustomerDbModel.rating >= rating,
                                                                        CustomerDbModel.status == status)
            case False, False:
                customers_db = db.session.query(CustomerDbModel).all()

        print(f'{customers_db=}')
        if customers_db:
            response = []
            for customer_db in customers_db:
                print(f'customer_db = {customer_db}')
                customer = Customer()
                customer.fromCustomerDbModel(customer_db)
                response.append(customer)
            print(response)
            return response, 200
        else:
            return 'nothing found', 404
    except exc.SQLAlchemyError:
        db.session.rollback()
        return 'server error', 500


def update_customer_by_id(body, customer_id):  # noqa: E501
    """Updates existing customer

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param customer_id: Customer&#x27;s ID
    :type customer_id: str

    :rtype: Customer
    """
    if connexion.request.is_json:
        try:
            body = Customer.from_dict(connexion.request.get_json())  # noqa: E501
            customer_db_resp = db.session.query(CustomerDbModel).filter(CustomerDbModel.id == customer_id).first()
            if customer_db_resp:
                customer_with_contact = db.session.query(CustomerDbModel).filter_by(contact=body.contact).first()
                print(f'{customer_with_contact=}')
                print(f'{customer_id=}')

                if customer_with_contact and customer_with_contact.id != int(customer_id):  # TODO
                    # db and server model still have different types of baker Id
                    db.session.rollback()
                    return "wrong contact, it is already being used", 400
                else:
                    customer_db_resp.name = body.name
                    customer_db_resp.rating = body.rating
                    customer_db_resp.status = body.status
                    customer_db_resp.contact = body.contact
                    db.session.commit()
                    response = Customer()
                    response.fromCustomerDbModel(customer_db_resp)
                    print(f'updated response = {response}')
                    return response, 200
            else:
                return 'customer with that id not found', 404

        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400
