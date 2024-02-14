from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Buyer(db.Model):
    __tablename__ = "buyer"
    buyer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.BigInteger(), unique=True)
    address = db.Column(db.Text())
    orders = db.relationship('Order', backref='buyer')


class Farmer(db.Model):
    __tablename__ = "farmer"
    farmer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.BigInteger(), unique=True)
    address = db.Column(db.Text())

    def __repr__(self):
        return f"<Farmer {self.username}>"

class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    is_out_of_stock = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text())
    image_link = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    category = db.relationship("Category", backref="products")
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    farmer = db.relationship('Farmer', backref='products')
    orders = db.relationship('Order', backref='product')

class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)

class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    buyer_name = db.Column(db.String(100))
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    review_date = db.Column(db.Date)

    product = db.relationship('Product', backref='reviews')

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    order_date = db.Column(db.DateTime)

class Notifications(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    email = db.Column(db.String(254), unique=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True)

