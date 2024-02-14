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
def create_farmer():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': True, 'message': 'Invalid JSON data in request'}), 400

        required_fields = ['username', 'password', 'email', 'phone', 'address']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': True, 'message': f'Missing or empty {field}'}), 400

        # Check if username already exists
        username = data['username']
        if Farmer.query.filter_by(username=username).first():
            return jsonify({'error': True, 'message': 'User already exists'}), 400

        # Create new buyer
        new_farmer = Farmer(**data) #dict to unpack keyword arguments
        db.session.add(new_farmer)
        db.session.commit()

        return jsonify({'id': new_farmer.farmer_id, 'name': new_farmer.username}), 201

    except Exception as e:
        return jsonify({'error': True, 'message': 'An error occurred while processing the request'}), 500


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
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': True, 'message': 'Invalid JSON data in request'}), 400

        required_fields = ['username', 'password', 'email', 'phone', 'address']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': True, 'message': f'Missing or empty {field}'}), 400

        # Check if username already exists
        username = data['username']
        if Buyer.query.filter_by(username=username).first():
            return jsonify({'error': True, 'message': 'User already exists'}), 400

        # Create new buyer
        new_buyer = Buyer(**data) #dict to unpack keyword arguments
        db.session.add(new_buyer)
        db.session.commit()

        return jsonify({'id': new_buyer.buyer_id, 'name': new_buyer.username}), 201

    except Exception as e:
        return jsonify({'error': True, 'message': 'An error occurred while processing the request'}), 500


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


@app.route("/update_buyer/<int:buyer_id>", methods=["PATCH"])
def patch_buyer(buyer_id):
    try:
        data = request.json

        #print("Received data:", data)  

        new_username = data.get("username")  
        new_password = data.get("password") 

        #print("New username:", new_username)  
        #print("New password:", new_password)  

        user = Buyer.query.get(buyer_id)

        if not user:
            return jsonify({"error": "Buyer not found"}), 404

        if new_username:
            user.username = new_username

        if new_password:
            user.password = new_password

        db.session.commit()

        return jsonify({"message": "Buyer information updated successfully"}), 200

    except Exception as e:
        #print("Error:", e)  
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(port=4000,debug=True)
