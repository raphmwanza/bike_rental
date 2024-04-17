from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import User, Bike
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'aHSGsMY7XHasgDHQM3MruhLuVWzdAJ7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Fi$ton2004@127.0.0.1/bike_rental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            return redirect(url_for('login', user_id=user.id))  # Redirect with user ID as URL parameter
        else:
            return 'Invalid email or password'

    bikes = Bike.query.all()
    return render_template('index.html', bikes=bikes)


# Login route
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    user_id = request.args.get('user_id')  # Retrieve user ID from URL parameter
    user = User.query.get(user_id)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            bikes = Bike.query.filter_by(bike_id=user.rent_id).all()
            bikes = Bike.query.filter_by(availability=1).all()
            return render_template('login.html', user=user, bikes=bikes)
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('your_template.html', user_id=user, bikes=bikes)


# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# Rent bike route
@app.route('/rent_bike/<int:user_id>/<int:bike_id>', methods=['POST'])
def rent_bike(user_id, bike_id):
    user = User.query.get(user_id)
    if user:
        bike = Bike.query.get(bike_id)
        if bike and bike.availability:
            bike.availability = False
            user.rent_id = bike_id
            db.session.commit()
            return 'Bike rented successfully!'
        else:
            return 'Bike not available.'

    return 'User not found'


# Return bike route
@app.route('/return_bike/<int:user_id>/<int:bike_id>')
def return_bike(user_id, bike_id):
    user = User.query.get(user_id)
    if user:
        bike = Bike.query.get(bike_id)
        if bike and bike.availability:
            bike.availability = True
            user.rent_id = bike_id
            db.session.commit()
            return 'Bike returned successfully!'
        else:
            return 'Bike Available.'

    return 'User not found'
    


if __name__ == '__main__':
    app.run(debug=True)
