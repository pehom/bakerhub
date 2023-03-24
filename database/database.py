from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def isContactExisted(table, contact):
    resp = db.session.query(table).filter_by(contact=contact).first()
    res = bool(resp)
    print(f'isContactExisted = {res}')
    return bool(resp)


def checkReviewAuthorId(table, author_id):
    resp = db.session.query(table).filter_by(author_id=author_id).first()
    print(resp)
    return bool(resp)


def checkProductTitle(table, title):
    resp = db.session.query(table).filter_by(title=title).first()
    print(resp)
    return bool(resp)


