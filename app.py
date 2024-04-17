from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import User, Bike
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Fi$ton2004@127.0.0.1/bike_rental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            # Redirect to a different route upon successful login
            return redirect(url_for('dashboard'))  # Assuming you have a 'dashboard' route
        else:
            return 'Invalid email or password'

    bikes = Bike.query.all()
    return render_template('index.html', bikes=bikes)


# Login route

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # If login successful, fetch customer information
            bikes = Bike.query.filter_by(rent_id=user.id).all()
            return render_template('login.html', user=user, bikes=bikes)
        else:
            # If login failed, return error message
            return render_template('login.html', error='Invalid email or password')

    # If GET request or login failed, render login page
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Rent bike route
@app.route('/rent_bike/<int:bike_id>')
def rent_bike(bike_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    bike = Bike.query.get(bike_id)
    if bike and bike.availability:
        bike.availability = False
        db.session.commit()
        return 'Bike rented successfully!'
    else:
        return 'Bike not available.'

# Return bike route
@app.route('/return_bike/<int:bike_id>')
def return_bike(bike_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    bike = Bike.query.get(bike_id)
    if bike and not bike.availability:
        bike.availability = True
        db.session.commit()
        return 'Bike returned successfully!'
    else:
        return 'Bike not rented or already returned.'

if __name__ == '__main__':
    app.run(debug=True)
