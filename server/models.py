from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class  Buyer(db.Model):
    __tablename__="buyer"
    buyer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email=db.Column(db.String(100),nullable=False)

    

class  Farmer(db.Model):
    __tablename__="farmer"
    farmer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.BigInteger(),unique=True)
    address=db.Column(db.Text())
    
    def __repr__(self):
        return f"<Farmer {self.first_name} {self.last_name}>"
    

class  Products(db.Model):
    __tablename__="products"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Float(), nullable=False)
    quantity=db.Column(db.Integer(),default=1)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    farmer = db.relationship('Farmer', backref='products')

    def __repr__(self):
        return f"<Product {self.product_name}>"


class Review(db.Model):
    __tablename__="reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    reviewer_name = db.Column(db.String(100))
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    review_date = db.Column(db.Date)

    product = db.relationship('Product', backref='reviews')

    def __repr__(self):
        return f"<Review for {self.product.product_name} by {self.reviewer_name}>"      

class Orders(db.Model):
    __tablename__="orders"

    order_id=db.Column(db.Integer, primary_key=True)
    Buyer_id=db.Column(db.Integer, primary_key=True)
    product_id=db.Column(db.Integer, primary_key=True)
    total_cost=db.Column(db.Integer, primary_key=True)

