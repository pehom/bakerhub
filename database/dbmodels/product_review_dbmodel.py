from database.database import db


class ProductReviewDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(100))
    product_id = db.Column(db.String(100))
    rating = db.Column(db.Integer())
    description = db.Column(db.Integer())

    def __repr__(self):
        return f'>>>>>ProductReview: \n \t {self.id=} \n \t {self.author_id=} ' \
               f'\n \t {self.product_id=}\n \t {self.rating=}\n \t {self.description=}'

