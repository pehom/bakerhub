from database.database import db


class CustomerDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    rating = db.Column(db.Numeric())
    status = db.Column(db.String(50))
    reviews_quantity = db.Column(db.Integer())
    rating_points = db.Column(db.Integer())

    def __repr__(self):
        return f'>>>>> Customer_db: \n \t {self.id=}\n \t {self.name=}\n \t {self.contact=}\n \t ' \
               f'{self.status=}\n \t {self.rating=}\n \t {self.rating_points=} \n \t {self.reviews_quantity=}\n'

    def updateRating(self):
        if self.reviews_quantity != 0:
            self.rating = self.rating_points / self.reviews_quantity
        else:
            self.rating = 0
            self.rating_points = 0
