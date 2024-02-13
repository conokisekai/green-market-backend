from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Orders, Farmer, Buyer, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
