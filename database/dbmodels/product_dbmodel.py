from database.database import db


class ProductDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baker_id = db.Column(db.String(100))
    title = db.Column(db.String())
    price = db.Column(db.String(50))
    status = db.Column(db.String(100))
    description = db.Column(db.String())
    ingredients = db.Column(db.String())
    execution = db.Column(db.String(100))
    rating = db.Column(db.Numeric())
    rating_points = db.Column(db.Integer())
    reviews_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f'>>>>> Product: \n \t {self.id=}\n \t {self.baker_id=}\n \t {self.title=}\n \t {self.price=} ' \
               f'\n \t {self.status=}\n \t {self.description=} \n \t {self.ingredients=} \n \t {self.execution=}' \
               f'\n \t {self.rating=} \n \t {self.rating_points=} \n \t {self.reviews_quantity=}'

    def updateRating(self):
        if self.reviews_quantity != 0:
            self.rating = self.rating_points / self.reviews_quantity
        else:
            self.rating = 0
            self.rating_points = 0
