from database.database import db


class OrderDbModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100))
    baker_id = db.Column(db.String(100))
    status = db.Column(db.String(100))
    price = db.Column(db.Numeric())
    products = db.Column(db.String())
    start_date = db.Column(db.String(100))

    def __repr__(self):
        return f'>>>>>Order: \n \t {self.id=}\n \t {self.customer_id=}\n \t {self.baker_id=}\n \t {self.status=}\n '\
               f'\t {self.price=}\n \t {self.products=}\n \t {self.start_date=} '
