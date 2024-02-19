from flask import Flask, jsonify, request
import json
from phone import send_otp
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Order, User, Review, Notifications
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


@app.route("/user_signup", methods=["POST"])
def create_user():
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
        new_user = User(
            username=data["username"],
            password=hashed_password,
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
        )
        db.session.add(new_user)
        db.session.commit()

        # Send OTP only once after adding the user
        send_otp(data["phone"], data["username"])

        return (
            jsonify(
                {
                    "id": new_user.user_id,
                    "name": new_user.username,
                    "OTP sent": True,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/user_login", methods=["POST"])
def user_login():
    try:
        data = request.get_json()
        if not data or "password" not in data:
            return jsonify({"error": True, "message": "Missing password"}), 400

        password = data["password"]
        user = User.query.filter(
            (User.username == data.get("username"))
            | (User.phone == data.get("phone"))
            | (User.email == data.get("email"))
        ).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
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
                    "user_type": "user",
                    "username": user.username,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/del_user_login/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


@app.route("/del_user_login/<user_id>", methods=["DELETE"])
def delete(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user deleted successfully"}), 200


@app.route("/update_user/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    try:
        data = request.json

        new_username = data.get("username")
        new_password = data.get("password")

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if new_username:
            user.username = new_username

        if new_password:
            user.password = new_password

        db.session.commit()

        return jsonify({"message": "User information updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run(port=4000, debug=True)
