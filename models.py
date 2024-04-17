from database import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))  # Corrected field name
    phone = db.Column(db.Integer)
    rent_id = db.Column(db.Integer, db.ForeignKey('bike_info.bike_id'))
    __tablename__ = 'customer_infos'
    
def set_password(self, password):
    self.password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.password, password)


class Bike(db.Model):
    __tablename__ = 'bike_info'  # Specify the table name explicitly
    bike_id = db.Column(db.Integer, primary_key=True)
    bike_name = db.Column(db.String(255))
    bike_type = db.Column(db.String(255))
    availability = db.Column(db.Boolean, default=True)
