from flask import Flask, request, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, hash_password, verify_password, auth_required, roles_required
from flask_cors import CORS  
from backend.models import *
from backend.config import Config

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
    app.security.datastore.find_or_create_role(name='admin', description='the superuser of app')
    app.security.datastore.find_or_create_role(name='customer', description='a person who avail services')
    app.security.datastore.find_or_create_role(name='professional', description='a professional who provide services')
    db.session.commit()
    
    if not app.security.datastore.find_user(email='harshit@admin.com'):
        user=app.security.datastore.create_user(email='harshit@admin.com', fullname='Harshit Tiwari', password=hash_password('admin123'), roles=['admin'])

    db.session.commit()


datastore = app.security.datastore

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')

    user=datastore.find_user(email=email)

    if user and any(role.name=='admin' for role in user.roles):
        if not verify_password(password, user.password):
            return jsonify({'message':"Invalid password"}), 400
    
        return jsonify({'message':'Login successfully', 'token':user.get_auth_token()}), 200
    return jsonify({'message':"Admin doesn't exist"}), 404

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
        return jsonify({'token': user.get_auth_token(), 'email': user.email}), 200 
    
    return jsonify({'message': 'Wrong password'}), 400

@app.route('/customer/dashboard', methods=['GET'])
@auth_required('token')
@roles_required('customer')
def customer_dashboard():
    return jsonify({'message': 'This is the dashboard of customer'}), 200


@app.route('/register_professional',methods=['POST'])
def register_professional():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    address = data.get('address')
    pincode = data.get('pincode')
    service_category = data.get('service_category')
    experience = data.get('experience')
    service_name = data.get('service_name')

    pro=datastore.find_user(email=email)
    if not pro:
        try:
            user=datastore.create_user(email=email, password=hash_password(password), fullname=fullname)
            role=datastore.find_role('professional')
            datastore.add_role_to_user(user, role)

            pro=Professional(email=user.email, address=address, pin_code=pincode, service_category=service_category, experience=experience, service_name=service_name)

            db.session.add(pro)
            db.session.commit()
            return jsonify({'message':'Registered Successfully'}), 200

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message":"Some error occured while registeration"}), 400

    return jsonify({'message':'User already exist'}), 400

@app.route('/available_services')
def services():
    services = Services.query.with_entities(Services.service_name).all()
    service_name = [service[0] for service in services]
    return jsonify({'service':service_name}), 200
            

if __name__ == '__main__':
    app.run() 
