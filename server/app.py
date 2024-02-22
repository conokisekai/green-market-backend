from flask import Flask, jsonify, request,make_response
import json,requests
from requests.auth import HTTPBasicAuth
from passlib.hash import sha256_crypt
import base64,urllib3
from phone import send_otp
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Order, User, Review, Notifications, Category, CartItem
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import User


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)

#config secret key
consumer_key='fSJKwEHnmoiV2NXAFFSMu1Ja5SOzZLTmCSnM5lWQNrkZELbG'
consumer_secret='EPuvMFL9g7p1FxGvsLoKuOtgX8YiyRMMnH73CeJGhjG1yfncMV5VOiKGIP17muIG'

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
        h = sha256_crypt.encrypt(data["password"])
        
        new_user = User(
            username=data["username"],
            password=data['password'],
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
             role=data["role"],
        )
        db.session.add(new_user)
        db.session.commit()

        # Send OTP only once after adding the user
        send_otp(data["phone"], data["username"])


        new_user_data = {
            
        'New_user_data':
        
          {
            'id':new_user.user_id ,
            'name': new_user.username,
            'address': new_user.address, 
            'contact': new_user.phone,
            'role': new_user.role,
            
        }
    }
        return jsonify(new_user_data),201

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/user_login", methods=["POST"])
def user_login():
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify! Missing email or password.',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query.filter_by(email = auth.get('email')).first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify! User does not exist',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    if  (user.password, auth.get('password')):
        # generates the JWT Token
            token = jwt.encode({
                'id': user.user_id,
                'name':user.username,
                'email':user.email,
                'phone':user.phone
                
                
            }, "secret", algorithm="HS256")
  
            return make_response(jsonify({
                'token' : token,
                'name': user.username,
                'email':user.email
                }), 201)
        # returns 403 if password is wrong
    return make_response(
            'Could not verify! Wrong password',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )
# decorator for verifying the JWT
def token_required(token):
    @wraps(token)
    def decorated():
        token = token
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, algorithm="HS256" )
            current_user = User.query\
                .filter_by(id = data['user_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  (current_user)
  
    return decorated
@app.route('/users', methods =['GET'])
def get_all_users():
    
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json 
        # to the response list
        output.append({
            'name' : user.username,
            'email' : user.email,
            'id': user.user_id
        })
  
    return jsonify({'users': output})
  
@app.route("/delete_user/<user_id>", methods=["DELETE"])

def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

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
    
#stkpush#
@app.route('/access_token')
def access_token():
    mpesa_auth_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data=(requests.get(mpesa_auth_url,auth=HTTPBasicAuth(consumer_key, consumer_secret))).json()
    return data
http=urllib3.PoolManager()
@app.route('/stkpush', methods=['POST'])
def stk():
    
    
    ac_token = access_token()
    print(ac_token)
    headers={
        'Authorization': f'Bearer sj3oo0OTILF9idf83DI1o5DCmvpL' 
        }
    Timestamp = datetime.now() 
    times = Timestamp.strftime( '%Y%m%d%H%M%S' )
    pas = '174379' + 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' + times
    password= base64.b64encode(pas.encode('utf-8'))


    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254768171426,
        "PartyB": 174379,
        "PhoneNumber": 254768171426,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "GREENMARKET",
        "TransactionDesc": "Payment of X" 
    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
    return response.json()

@app.route("/del_user_login/<user_id>", methods=["DELETE"])
def delete(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user deleted successfully"}), 200



if __name__ == "__main__":
    app.run(port=4000, debug=True)
