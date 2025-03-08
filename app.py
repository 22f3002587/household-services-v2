from flask import Flask, request, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, hash_password, verify_password, auth_required, roles_required, current_user
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


#-----------------------------  Admin Related Routes  ------------------------------------------------
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

@app.route('/admin_home')
@auth_required('token')
@roles_required('admin')
def admin_home():
    services = Services.query.all()
    service_list = [{"service_id":service.service_id, "service_name":service.service_name, "service_category":service.service_category, "price":service.base_price, "expected_time":service.expected_time, "description":service.description} for service in services]

    professional = User.query.filter(User.roles.any(Role.name == "professional")).all()
    prolist = []
    for pro in professional:
        pro_detail = Professional.query.filter_by(user_id=pro.id).first()
        if pro_detail:
            prolist.append({"id":pro.id, "email":pro.email, "name":pro.fullname, "experience":pro_detail.experience, "service_name":pro_detail.service_name, "status":pro_detail.status})

    customer = User.query.filter(User.roles.any(Role.name == "customer")).all()
    customlist =[]
    for custom in customer:
        custom_detail = Customer.query.filter_by(user_id=custom.id).first()
        if custom_detail:
            customlist.append({"id": custom.id, "email":custom.email, "name":custom.fullname, "address":custom_detail.address, "pincode":custom_detail.pin_code, "contact":custom_detail.contact, "status":custom_detail.status})     

    # serv_req = Service_Request.query.all()
    # serv_reqlist = [{"service_id":serv_req.service_id, "customer_id":serv_req.customer_id, "pro_id":serv_req.professional_id, "status":serv_req.status}]
    

    return jsonify({"services":service_list, "professional":prolist, "customer":customlist}), 200 


@app.route('/admin/create_service', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def create_service():
    data = request.get_json()
    if not Services.query.filter_by(service_name=data["service_name"].title()).first():
        new_service = Services(
        service_category=data["service_category"],
        service_name=data["service_name"],
        expected_time=data["expected_time"],
        description=data["description"],
        base_price=data["base_price"]
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"message": "Service Created Successfully!"}), 201
    
    return jsonify({"message":"Service already exist"}), 400


@app.route('/admin/update_service/<int:service_id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def update_service(service_id):
    data = request.get_json()
    print(data)
    service = Services.query.get(service_id)
    
    if not service:
        return jsonify({"message": "Service not found"}), 404

    if 'service_name' in data:
        service.service_name = data["service_name"]
    if 'description' in data:
        service.description = data["description"]
    if 'price' in data:
        service.base_price = data["price"]
    if 'expected_time' in data:
        service.expected_time = data["expected_time"]

    
    db.session.commit()
    return jsonify({"message": "Service updated successfully!"}), 200

@app.route('/available_services')
def services():
    services=[]
    service_data = Services.query.all()
    for service in service_data:
        services.append(service.service_name)

    return jsonify({
        "services":services
    })    


#------------------------  Customer Related Routes  ------------------------------------------------
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

            customer = Customer(user_id=user.id, address=address, contact=contact, pin_code=pincode)

            db.session.add(customer)
            db.session.commit()
            return jsonify({'message': 'Registered Successfully'}), 200
            
        except Exception as e:
            print(e)
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

@app.route('/customer_dashboard', methods=['GET'])
@auth_required('token')
@roles_required('customer')
def customer_dashboard():
                 
    customer=current_user
    return jsonify({"name":customer.fullname, "email":customer.email}), 200
    


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

            pro=Professional(user_id=user.id, address=address, pin_code=pincode, service_category=service_category, experience=experience, service_name=service_name)

            db.session.add(pro)
            db.session.commit()
            return jsonify({'message':'Registered Successfully'}), 200

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message":"User already exist"}), 400

    # return jsonify({'message':'User already exist'}), 400


@app.route('/login_professional', methods=['POST'])
def login_professional():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    pro = datastore.find_user()
    user = datastore.find_user(email=email)
    if not user:
        return jsonify({'message': 'User does not exist'}), 404 

    if verify_password(password, user.password):
        return jsonify({'token': user.get_auth_token(), 'email': user.email}), 200 
    
    return jsonify({'message': 'Wrong password'}), 400

            

if __name__ == '__main__':
    app.run() 
