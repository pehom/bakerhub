from database.database import db


class BakerDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    status = db.Column(db.String(100))
    finished_orders = db.Column(db.Integer())
    rating = db.Column(db.Numeric())
    rating_points = db.Column(db.Integer())
    reviews_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f'\n>>>>> Baker: \n \t {self.id=}\n \t {self.name=}\n \t {self.contact=}\n \t {self.status=}\n ' \
               f'\t {self.rating=}\n \t {self.finished_orders=} \n \t {self.reviews_quantity=}'

    def updateRating(self):
        if self.reviews_quantity != 0:
            self.rating = self.rating_points / self.reviews_quantity
        else:
            self.rating = 0
            self.rating_points = 0
