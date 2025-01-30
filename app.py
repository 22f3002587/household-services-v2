from flask import Flask, request, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, hash_password, verify_password, auth_required
from flask_cors import CORS  
from backend.models import db, User, Role, Customer
from backend.config import Config
from backend.db_init import init_db

def CreateApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/*":{"origin":"http://localhost:8080"}})

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()

    return app

app = CreateApp()

with app.app_context():
    db.create_all()
    init_db()        

datastore = app.security.datastore

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')

    user=datastore.find_user(email=email)
    # print(verify_password(password, user.password))
    if not user:
        return jsonify({'message':"admin doesn't exist"}), 404
    
    if user.password!=password:
        return jsonify({'message':"invalid password"}), 400
    
    return jsonify({'message':'login successfully'}), 200


@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    address = data.get('address')
    contact = data.get('contact')
    pincode = data.get('pincode')


    if datastore.find_user(email=email) is None:
        try:
            
            user = datastore.create_user(email=email, password=hash_password(password), fullname=fullname)
            role=datastore.find_role('customer')
            datastore.add_role_to_user(user,role)

            customer = Customer(email=user.email, address=address, contact=contact, pin_code=pincode)

            db.session.add(customer)
            db.session.commit()
            return jsonify({'message': 'Registered Successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Some error occurred'}), 400
    
    else:
        return jsonify({'message': 'User already exists'}), 400
    

@app.route('/login_customer', methods=['POST'])
def custom_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = datastore.find_user(email=email)
    if not user:
        return jsonify({'message': 'User does not exist'}), 404 

    if verify_password(password, user.password):
        return jsonify({'token': user.get_auth_token(), 'email': user.email}), 200  # Change status code to 200 for success
    
    return jsonify({'message': 'Wrong password'}), 400

@app.route('/customer/dashboard', methods=['GET'])
@auth_required('token')
def customer_dashboard():
    return jsonify({'message': 'This is the dashboard of customer'}), 200

if __name__ == '__main__':
    app.run() 
