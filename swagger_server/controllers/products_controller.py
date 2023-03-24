import connexion
import six
from sqlalchemy import exc
from database.database import db
from database.dbmodels.product_dbmodel import ProductDbModel
from database.dbmodels.product_review_dbmodel import ProductReviewDbModel
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server.models.product_review import ProductReview  # noqa: E501
from swagger_server import util


def create_product(body):  # noqa: E501
    """Creates a new product

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Product
    """
    if connexion.request.is_json:
        body = Product.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            new_product_db = body.toProductDbModel()

            is_product_existed = db.session.query(ProductDbModel).filter_by(baker_id=new_product_db.baker_id,
                                                                            title=new_product_db.title).first()
            print(f'{is_product_existed=}')
            if is_product_existed:
                return 'product with that title already exists', 400
            else:
                new_product_db.rating = 0
                new_product_db.rating_points = 0
                new_product_db.reviews_quantity = 0
                print(f'{new_product_db=}')
                db.session.add(new_product_db)
                db.session.commit()
                resp_db = db.session.query(ProductDbModel).filter_by(baker_id=new_product_db.baker_id,
                                                                     title=new_product_db.title).first()
                print(f'{resp_db=}')
                resp = Product()
                resp.fromProductDbModel(resp_db)
                print(f'{resp=}')
                return resp, 200
        except exc.SQLAlchemyError:
            return 'server error', 500
    else:
        return 'bad request', 400


def create_product_review(body, product_id):  # noqa: E501
    """Creates product review

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param product_id: Product&#x27;s ID
    :type product_id: str

    :rtype: ProductReview
    """
    if connexion.request.is_json:
        body = ProductReview.from_dict(connexion.request.get_json())  # noqa: E501
        product_review_dbmodel = body.toProductReviewDbModel()
        product_review_dbmodel.product_id = product_id
        print(f'{product_review_dbmodel=}')
        try:
            author_id = product_review_dbmodel.author_id
            is_product_existed = bool(db.session.query(ProductDbModel).filter_by(id=product_id).first())
            print(f'{is_product_existed=}')
            if not is_product_existed:
                return 'bad request: no product with that id', 400
            else:
                review_db = db.session.query(ProductReviewDbModel).filter_by(author_id=author_id,
                                                                             product_id=product_id).first()
                # print(f'review_db = {review_db}')
                if review_db:
                    prev_rating = review_db.rating
                    resp_db = db.session.query(ProductReviewDbModel).filter_by(author_id=author_id).first()
                    resp_db.rating = product_review_dbmodel.rating
                    resp_db.description = product_review_dbmodel.description
                    db.session.commit()
                    # print(f'>>>resp_db = {resp_db}')
                    # print(f'>>>>prev rating = {prev_rating}')
                    resp = ProductReview()
                    resp.fromProductReviewDbModel(resp_db)
                    product_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
                    product_db.rating_points -= prev_rating
                    product_db.rating_points += product_review_dbmodel.rating
                    product_db.updateRating()
                    db.session.commit()
                    return resp, 200
                else:
                    db.session.add(product_review_dbmodel)
                    db.session.commit()
                    resp_db = db.session.query(ProductReviewDbModel).filter_by(author_id=author_id).first()
                    resp = ProductReview()
                    resp.fromProductReviewDbModel(resp_db)
                    product_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
                    # print(f'{product_db}')
                    product_db.rating_points += product_review_dbmodel.rating
                    product_db.reviews_quantity += 1
                    product_db.updateRating()
                    db.session.commit()
                    # print(f'{product_db}')
                    return resp, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400


def delete_product_by_id(product_id):  # noqa: E501
    """delete_product_by_id

    Deletes product with requested Id # noqa: E501

    :param product_id: Product&#x27;s ID
    :type product_id: str

    :rtype: None
    """
    print(f'{product_id=} ')
    product_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
    print(f'{product_db=}')
    if product_db:
        try:
            db.session.delete(product_db)
            db.session.commit()
            return {}, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    return 'no product with that id found', 404


def delete_product_review_by_id(product_id, review_id):  # noqa: E501
    """Deletes product review

     # noqa: E501

    :param product_id: Product&#x27;s ID
    :type product_id: str
    :param review_id: Review&#x27;s ID
    :type review_id: str

    :rtype: None
    """
    print(f'{product_id=} \n {review_id=}')
    try:
        review_db = db.session.query(ProductReviewDbModel).filter_by(id=review_id).first()
        prev_rating = review_db.rating
        print(f'{review_db=}')
        if review_db:
            db.session.delete(review_db)
            product_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
            product_db.rating_points -= prev_rating
            product_db.reviews_quantity -= 1
            product_db.updateRating()
            db.session.commit()
            return {}, 200
        return 'no review found', 404
    except exc.SQLAlchemyError:
        db.session.rollback()
        return 'server error', 500


def get_product_by_id(product_id):  # noqa: E501
    """Returns product with requested ID

     # noqa: E501

    :param product_id: Product&#x27;s ID
    :type product_id: str

    :rtype: Product
    """
    try:
        product_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
        print(product_db)
        if product_db:
            resp = Product()
            resp.fromProductDbModel(product_db)
            return resp, 200
        else:
            return 'no customer found for that id', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_product_reviews_by_product_id(product_id):  # noqa: E501
    """Returns product reviews

     # noqa: E501

    :param product_id: Product&#x27;s ID
    :type product_id: str

    :rtype: List[ProductReview]
    """
    try:
        reviews_db = db.session.query(ProductReviewDbModel).filter_by(product_id=product_id).all()
        print(reviews_db)
        if reviews_db:
            response = []
            for review in reviews_db:
                resp = ProductReview()
                resp.fromProductReviewDbModel(review)
                response.append(resp)
            return response, 200
        else:
            return [], 200  # TODO maybe it should be an error: 'no reviews found for that product', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_products(title=None, baker_id=None, rating=None):  # noqa: E501
    """Returns products of all bakers

     # noqa: E501

    :param title: 
    :type title: str
    :param baker_id: 
    :type baker_id: str
    :param rating: 
    :type rating: float

    :rtype: List[Product]
    """
    try:
        print(f'>>>>>get products: \n {title=} \n {baker_id=} \n {rating=}')
        products_db = []

        match bool(title), bool(baker_id), bool(rating):
            case True, False, False:
                products_db = db.session.query(ProductDbModel).filter(ProductDbModel.title == title)
            case True, True, False:
                product_db = db.session.query(ProductDbModel).filter_by(title=title, baker_id=baker_id).first()
                if product_db:
                    products_db.append(product_db)
            case False, True, False:
                products_db = db.session.query(ProductDbModel).filter(ProductDbModel.baker_id == baker_id)
            case True, False, True:
                products_db = db.session.query(ProductDbModel).filter(ProductDbModel.title == title,
                                                                      ProductDbModel.rating >= rating)
            case False, False, True:
                products_db = db.session.query(ProductDbModel).filter(ProductDbModel.rating >= rating)
            case False, False, False:
                products_db = db.session.query(ProductDbModel).all()

        print(f'{products_db=}')
        if products_db:
            response = []
            for product_db in products_db:
                print(f'{products_db=}')
                product = Product()
                product.fromProductDbModel(product_db)
                response.append(product)
            print(response)
            return response, 200
        else:
            return [], 200  # TODO may be it should be an error 'nothing found', 404
    except exc.SQLAlchemyError:
        db.session.rollback()
        return 'server error', 500


def update_product_by_id(body, product_id):  # noqa: E501
    """Updating existing product

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param product_id: Product&#x27;s ID
    :type product_id: str

    :rtype: Product
    """
    if connexion.request.is_json:
        try:
            body = Product.from_dict(connexion.request.get_json())  # noqa: E501
            product_db_resp = db.session.query(ProductDbModel).filter(ProductDbModel.id == product_id).first()
            if product_db_resp:
                is_title_valid = db.session.query(ProductDbModel).filter_by(baker_id=body.baker_id,
                                                                            title=body.title).first()
                print(f'{is_title_valid=}')
                if is_title_valid and is_title_valid.id != int(product_id):
                    return "wrong title: product with that title already exists", 400
                else:
                    product_db_resp.description = body.description
                    product_db_resp.execution = body.execution
                    product_db_resp.ingredients = body.ingredients
                    product_db_resp.price = body.price
                    product_db_resp.status = body.status
                    product_db_resp.title = body.title
                    db.session.commit()
                    resp_db = db.session.query(ProductDbModel).filter_by(id=product_id).first()
                    response = Product()
                    response.fromProductDbModel(resp_db)
                    print(f'updated response = {response}')
                    return response, 200
            else:
                return 'product with that id not found', 404

        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400

