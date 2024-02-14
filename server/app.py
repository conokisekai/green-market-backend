from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Order, Farmer, Buyer, Review, Notifications

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate=Migrate(app,db)
db.init_app(app)


@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
