from flask import Flask, jsonify, request
import json
from phone import send_otp
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Order, Farmer, Buyer, Review, Notifications
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def home():
    data = {"Server side": "Checkers"}
    return jsonify(data), 200


@app.route("/farmer_signup", methods=["POST"])
def create_farmer():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        required_fields = ["username", "password", "email", "phone", "address"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify({"error": True, "message": f"Missing or empty {field}"}),
                    400,
                )

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )
        new_farmer = Farmer(
            username=data["username"],
            password=hashed_password,
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
        )
        db.session.add(new_farmer)
        db.session.commit()

        # Send OTP only once after adding the farmer
        send_otp(data["phone"], data["username"])

        return (
            jsonify(
                {
                    "id": new_farmer.farmer_id,
                    "name": new_farmer.username,
                    "OTP sent": True,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/farmer_login", methods=["POST"])
def farmer_login():
    try:
        data = request.get_json()
        if not data or "password" not in data:
            return jsonify({"error": True, "message": "Missing password"}), 400

        password = data["password"]
        farmer = Farmer.query.filter(
            (Farmer.username == data.get("username"))
            | (Farmer.phone == data.get("phone"))
            | (Farmer.email == data.get("email"))
        ).first()

        if not farmer or not bcrypt.check_password_hash(farmer.password, password):
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Invalid username, phone, email, or password",
                    }
                ),
                401,
            )

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user_type": "farmer",
                    "username": farmer.username,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/buyer_signup", methods=["POST"])
def create_buyer():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        required_fields = ["username", "password", "email", "phone", "address"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify({"error": True, "message": f"Missing or empty {field}"}),
                    400,
                )

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )
        new_buyer = Buyer(
            username=data["username"],
            password=hashed_password,
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
        )
        db.session.add(new_buyer)
        db.session.commit()

        # Send OTP only once after adding the buyer
        send_otp(data["phone"], data["username"])

        return (
            jsonify(
                {
                    "id": new_buyer.buyer_id,
                    "name": new_buyer.username,
                    "OTP sent": True,
                }
            ),
            201,
        )

    except IntegrityError as e:
        db.session.rollback()  # Rollback the transaction
        return jsonify({"error": True, "message": f"Username already exists"}), 409
    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500
    except IntegrityError as e:
        db.session.rollback()  # Rollback the transaction
        return jsonify({"error": True, "message": f"Username already exists"}), 409
    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/buyer_login", methods=["POST"])
def buyer_login():
    try:
        data = request.get_json()
        if not data or "password" not in data:
            return jsonify({"error": True, "message": "Missing password"}), 400

        password = data["password"]
        buyer = Buyer.query.filter(
            (Buyer.username == data.get("username"))
            | (Buyer.phone == data.get("phone"))
            | (Buyer.email == data.get("email"))
        ).first()

        if not buyer or not bcrypt.check_password_hash(buyer.password, password):
            return (
                jsonify(
                    {
                        "error": True,
                        "message": "Invalid username, phone, email, or password",
                    }
                ),
                401,
            )

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user_type": "buyer",
                    "username": buyer.username,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


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

        new_username = data.get("username")
        new_password = data.get("password")

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
        return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run(port=4000, debug=True)
