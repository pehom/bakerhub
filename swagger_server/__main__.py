#!/usr/bin/env python3

import connexion
from database.database import db
from swagger_server import encoder

conn_app = connexion.App(__name__, specification_dir='./swagger/')
conn_app.app.json_encoder = encoder.JSONEncoder
conn_app.add_api('swagger.yaml', arguments={'title': 'Bakers hub OpenAPI spec'}, pythonic_params=True)

app = conn_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
