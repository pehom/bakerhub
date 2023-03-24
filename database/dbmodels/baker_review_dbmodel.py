from database.database import db


class BakerReviewDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baker_id = db.Column(db.String(100))
    author_id = db.Column(db.String(100))
    rating = db.Column(db.Integer())
    description = db.Column(db.Integer())

    def __repr__(self):
        return f'>>>>> BakerReview: \n \t {self.id=}\n \t {self.baker_id=}\n \t {self.author_id=} ' \
               f'\t {self.rating=}\n \t {self.description=}'

