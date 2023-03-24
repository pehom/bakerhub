import connexion
import six

from database.database import isContactExisted, db
from database.dbmodels.baker_dbmodel import BakerDbModel
from database.dbmodels.baker_review_dbmodel import BakerReviewDbModel
from swagger_server.models.baker import Baker  # noqa: E501
from swagger_server.models.baker_review import BakerReview  # noqa: E501
from sqlalchemy import exc
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server import util


def create_baker(body):  # noqa: E501
    """Creates a new baker

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Baker
    """
    if connexion.request.is_json:
        body = Baker.from_dict(connexion.request.get_json())  # noqa: E501
        print(f'request body ={body}')
        new_baker = body.toBakerDbModel()
        new_baker.rating = 0
        new_baker.rating_points = 0
        new_baker.reviews_quantity = 0
        print(f'new_baker_db = {new_baker}')
        contact = new_baker.contact
        if isContactExisted(BakerDbModel, contact):
            return 'bad request: this contact is already been used', 400
        else:
            try:
                db.session.add(new_baker)
                db.session.commit()
                resp_db = db.session.query(BakerDbModel).filter_by(contact=contact, name=new_baker.name).first()
                resp = Baker()
                resp.fromBakerDbModel(resp_db)
                return resp, 200
            except exc.SQLAlchemyError:
                db.session.rollback()
                return 'server error', 500
    else:
        return 'bad request', 400


def create_baker_review(body, baker_id):  # noqa: E501
    """Creates baker review

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param baker_id: Baker&#x27;s ID
    :type baker_id: str

    :rtype: BakerReview
    """
    if connexion.request.is_json:
        body = BakerReview.from_dict(connexion.request.get_json())  # noqa: E501
        baker_review_dbmodel = body.toBakerReviewDbModel()
        baker_review_dbmodel.baker_id = baker_id
        try:
            author_id = baker_review_dbmodel.author_id
            is_baker_existed = bool(db.session.query(BakerDbModel).filter_by(id=baker_id).first())
            if not is_baker_existed:
                return 'bad request: no baker with that id', 400
            else:
                review_db = db.session.query(BakerReviewDbModel).filter_by(author_id=author_id,
                                                                           baker_id=baker_id).first()
                print(f'review_db = {review_db}')
                if review_db:
                    prev_rating = review_db.rating
                    resp_db = db.session.query(BakerReviewDbModel).filter_by(author_id=author_id).first()
                    resp_db.rating = baker_review_dbmodel.rating
                    resp_db.description = baker_review_dbmodel.description
                    db.session.commit()
                    print(f'>>>resp_db = {resp_db}')
                    print(f'>>>>prev rating = {prev_rating}')
                    resp = BakerReview()
                    resp.fromBakerReviewDbModel(resp_db)
                    baker_db = db.session.query(BakerDbModel).filter_by(id=baker_id).first()
                    baker_db.rating_points -= prev_rating
                    baker_db.rating_points += baker_review_dbmodel.rating
                    baker_db.updateRating()
                    db.session.commit()
                    return resp, 200
                else:
                    db.session.add(baker_review_dbmodel)
                    db.session.commit()
                    resp_db = db.session.query(BakerReviewDbModel).filter_by(author_id=author_id).first()
                    resp = BakerReview()
                    resp.fromBakerReviewDbModel(resp_db)
                    baker_db = db.session.query(BakerDbModel).filter_by(id=baker_id).first()
                    print(baker_db)
                    baker_db.rating_points += baker_review_dbmodel.rating
                    baker_db.reviews_quantity += 1
                    baker_db.updateRating()
                    print(baker_db)
                    db.session.commit()
                    return resp, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400


def delete_baker_by_id(baker_id):  # noqa: E501
    """delete_baker_by_id

    Deletes baker with requested ID # noqa: E501

    :param baker_id: Baker&#x27;s ID
    :type baker_id: str

    :rtype: None
    """
    print(f'{baker_id=}')
    baker = db.session.query(BakerDbModel).filter_by(id=baker_id).first()
    print(f'baker_db = {baker}')
    if baker:
        try:
            db.session.delete(baker)
            db.session.commit()
            return {}, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    return 'baker with that id not found', 404


def delete_baker_review_by_id(baker_id, review_id):  # noqa: E501
    """Deletes baker review

     # noqa: E501

    :param baker_id: Baker&#x27;s ID
    :type baker_id: str
    :param review_id: Review&#x27;s ID
    :type review_id: str

    :rtype: None
    """
    print(f'{baker_id=} \n {review_id=}')
    review_db = db.session.query(BakerReviewDbModel).filter_by(baker_id=baker_id, id=review_id).first()
    prev_rating = review_db.rating
    print(f'{review_db=}')
    if review_db:
        try:
            db.session.delete(review_db)
            baker_db = db.session.query(BakerDbModel).filter_by(id=baker_id).first()
            baker_db.rating_points -= prev_rating
            baker_db.reviews_quantity -= 1
            baker_db.updateRating()
            db.session.commit()
            return {}, 200
        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    return 'no review found', 404


def get_baker_reviews_by_baker_id(baker_id):  # noqa: E501
    """Returns baker reviews

     # noqa: E501

    :param baker_id: Baker&#x27;s ID
    :type baker_id: str

    :rtype: List[BakerReview]
    """
    try:
        reviews_db = db.session.query(BakerReviewDbModel).filter_by(baker_id=baker_id).all()
        print(reviews_db)
        if reviews_db:
            response = []
            for review in reviews_db:
                resp = BakerReview()
                resp.fromBakerReviewDbModel(review)
                response.append(resp)
            return response, 200
        else:
            return 'no reviews found for that baker id', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_baker_by_id(baker_id):  # noqa: E501
    """Returns baker with requested ID

     # noqa: E501

    :param baker_id: Baker&#x27;s id
    :type baker_id: str

    :rtype: Baker
    """
    try:
        baker_db = db.session.query(BakerDbModel).filter_by(id=baker_id).first()
        print(baker_db)
        if baker_db:
            resp = Baker()
            resp.fromBakerDbModel(baker_db)
            return resp, 200
        else:
            return 'no baker found for that id', 404
    except exc.SQLAlchemyError:
        return 'server error', 500


def get_bakers(status=None, rating=None):  # noqa: E501
    """Returns list of bakers

     # noqa: E501

    :param status: Bakers&#x27; status
    :type status: str
    :param rating: Baker&#x27;s rating
    :type rating: float

    :rtype: List[Baker]
    """
    try:
        print(f'{status=}, {rating=}')
        bakers_db = []
        match bool(status), bool(rating):
            case True, True:
                bakers_db = db.session.query(BakerDbModel).filter(BakerDbModel.status == status,
                                                                  BakerDbModel.rating >= rating)
            case False, True:
                bakers_db = db.session.query(BakerDbModel).filter(BakerDbModel.rating >= rating)
            case True, False:
                bakers_db = db.session.query(BakerDbModel).filter(BakerDbModel.status == status)
            case False, False:
                bakers_db = db.session.query(BakerDbModel).all()

        print(f'{bakers_db=}')
        if bakers_db:
            response = []
            for baker_db in bakers_db:
                print(f'{baker_db}')
                baker = Baker()
                baker.fromBakerDbModel(baker_db)
                response.append(baker)
            print(f'{response=}')
            return response, 200
        else:
            return 'nothing found', 404
    except exc.SQLAlchemyError:
        db.session.rollback()
        return 'server error', 500


def update_baker_by_id(body, baker_id):  # noqa: E501
    """Updates existing baker

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param baker_id: Baker&#x27;s ID
    :type baker_id: str

    :rtype: Baker
    """
    if connexion.request.is_json:
        try:
            body = Baker.from_dict(connexion.request.get_json())  # noqa: E501
            baker_db_resp = db.session.query(BakerDbModel).filter(BakerDbModel.id == baker_id).first()
            if baker_db_resp:
                baker_with_contact = db.session.query(BakerDbModel).filter_by(contact=body.contact).first()
                print(f'{baker_with_contact=}')
                print(f'{baker_id=}')
                if baker_with_contact and baker_with_contact.id != int(
                        baker_id):  # TODO db and server model still have different types of baker Id
                    db.session.rollback()
                    return "wrong contact, it is already being used", 400
                else:
                    baker_db_resp.name = body.name
                    baker_db_resp.status = body.status
                    baker_db_resp.contact = body.contact
                    db.session.commit()
                    response = Baker()
                    response.fromBakerDbModel(baker_db_resp)
                    print(f'updated response = {response}')
                    return response, 200
            else:
                return 'baker with that id not found', 404

        except exc.SQLAlchemyError:
            db.session.rollback()
            return 'server error', 500
    else:
        return 'bad request', 400
