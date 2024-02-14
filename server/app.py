from flask import Flask,jsonify,request
import json
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


@app.route('/farmer_signup', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email=data['email']
    phone=data['phone']
    address=data['address']

    user = Farmer.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': True, 'message': 'user already exists'}), 400
    new_user = Farmer(username=username, email=email,password=password,phone=phone, address=address)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.farmer_id, "name":new_user.username})


@app.route('/farmer_login', methods=['POST'])
def farmer_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    
    user = Farmer.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404


    if user.password != password:
        return jsonify({'error': 'Invalid password'}), 401


    user_details = {
        'Farmer_id': user.farmer_id,
        'username': user.username,
        
    }

    return jsonify(user_details), 200


@app.route('/buyer_signup', methods=['POST'])
def create_buyer():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email=data['email']
    phone=data['phone']
    address=data['address']


    user = Buyer.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': True, 'message': 'user already exists'}), 400
    new_user = Buyer(username=username, email=email,password=password,phone=phone, address=address)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, "name":new_user.username})


@app.route('/buyer_login', methods=['POST'])
def buyer_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = Buyer.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.password != password:
        return jsonify({'error': 'Invalid password'}), 401

    user_details = {
        'buyer_id': user.buyer_id,
        'username': user.username,
        
    }

    return jsonify(user_details), 200


@app.route("/del_buyer_login/<buyer_id>", methods=["DELETE"])
def delete_buyer(buyer_id):
    user = Buyer.query.filter_by(buyer_id=buyer_id).first()

    if not user:
        return jsonify({"error": "Buyer not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Buyer deleted successfully"}), 200


@app.route("/del_farmer_login/<farmer_id>", methods=["DELETE"])
def delete_farmer(farmer_id):
    user = Farmer.query.filter_by(farmer_id=farmer_id).first()

    if not user:
        return jsonify({"error": "Farmer not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Farmer deleted successfully"}), 200



if __name__ == '__main__':
    app.run(port=4000,debug=True)
