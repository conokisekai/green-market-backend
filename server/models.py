from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class  Buyer(db.Model):
    __tablename__="buyer"
    buyer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.BigInteger(),unique=True)
    address=db.Column(db.Text())
    buyer = db.relationship('Buyer', backref='orders')




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
    

class  Product(db.Model):
    __tablename__="product"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Float(), nullable=False)
    quantity=db.Column(db.Integer(),default=1)
    is_out_of_stock=db.Column(db.Boolean, default=False)
    description=db.Column(db.Text())
    image_link=db.Column(db.String(500))
    category_id=db.Column(db.Integer,db.ForeignKey("category.category_id"))
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    farmer = db.relationship('Farmer', backref='products')
    product = db.relationship('Products', backref='orders')


class Review(db.Model):
    __tablename__="review"

    review_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    buyer_name = db.Column(db.String(100))
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    review_date = db.Column(db.Date)

    product = db.relationship('Product', backref='reviews')

   
class Orders(db.Model):
    __tablename__="orders"

    order_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    total_cost = db.Column(db.Integer)
