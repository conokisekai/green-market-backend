from faker import Faker
from myapp import db, Buyer, Farmer, Product, Review

fake = Faker()

# Function to generate dummy buyers
def generate_buyers(num_buyers):
    for _ in range(num_buyers):
        buyer = Buyer(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address()
        )
        db.session.add(buyer)
    db.session.commit()

# Function to generate dummy farmers
def generate_farmers(num_farmers):
    for _ in range(num_farmers):
        farmer = Farmer(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address()
        )
        db.session.add(farmer)
    db.session.commit()

# Function to generate dummy products
def generate_products(num_products, num_farmers):
    for _ in range(num_products):
        farmer_id = randint(1, num_farmers)
        product = Products(
            product_name=fake.word(),
            price=fake.random_number(digits=2),
            quantity=fake.random_number(digits=2),
            out_of_stock=fake.boolean(chance_of_getting_true=50),
            description=fake.text(),
            image_link=fake.image_url(),
            category_id=randint(1, 10),  # Adjust as needed
            farmer_id=farmer_id
        )
        db.session.add(product)
    db.session.commit()

# Function to generate dummy reviews
def generate_reviews(num_reviews, num_products):
    for _ in range(num_reviews):
        product_id = randint(1, num_products)
        review = Review(
            product_id=product_id,
            buyer_name=fake.name(),
            review_text=fake.text(),
            rating=randint(1, 5),
            review_date=fake.date()
        )
        db.session.add(review)
    db.session.commit()

if __name__ == '__main__':
  