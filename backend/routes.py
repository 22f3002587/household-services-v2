from flask import request, jsonify
from flask_security import auth_required, roles_required, current_user, hash_password, verify_password
from backend.models import db, Services, User, Role, Professional, Customer, Service_Request
from sqlalchemy import or_, func
import uuid
from datetime import datetime as dt, timedelta

def create_routes(app):
    # Admin Routes
    @app.route('/admin_login', methods=['POST'])
    def admin_login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = app.security.datastore.find_user(email=email)

        if user and any(role.name == 'admin' for role in user.roles):
            if not verify_password(password, user.password):
                return jsonify({'message': "Invalid password"}), 400

            return jsonify({'message': 'Login successfully', 'token': user.get_auth_token()}), 200
        return jsonify({'message': "Admin doesn't exist"}), 404

    @app.route('/admin_home')
    @auth_required('token')
    @roles_required('admin')
    def admin_home():
        services = Services.query.all()
        service_list = [{"service_id": service.service_id, "service_name": service.service_name,
                         "service_category": service.service_category, "price": service.base_price,
                         "expected_time": service.expected_time, "description": service.description}
                        for service in services]

        professional = User.query.filter(User.roles.any(Role.name == "professional")).all()
        prolist = []
        for pro in professional:
            pro_detail = Professional.query.filter_by(user_id=pro.id).first()
            if pro_detail:
                prolist.append({"id": pro.id, "email": pro.email, "name": pro.fullname,
                                "experience": pro_detail.experience, "service_name": pro_detail.service_name,
                                "status": pro_detail.status, "is_active":pro.active, "address": pro_detail.address})

        customer = User.query.filter(User.roles.any(Role.name == "customer")).all()
        customlist = []
        for custom in customer:
            custom_detail = Customer.query.filter_by(user_id=custom.id).first()
            if custom_detail:
                customlist.append({"id": custom.id, "email": custom.email, "name": custom.fullname,
                                   "address": custom_detail.address, "pincode": custom_detail.pin_code,
                                   "contact": custom_detail.contact, "gender": custom_detail.gender, "is_active":custom.active})

        serv_req_list =[]
        serv_req = Service_Request.query.all()
        for req in serv_req:
            customer_email = User.query.get(req.customer_id).email
            pro_email = User.query.get(req.professional_id).email
            service_name = Services.query.get(req.service_id).service_name
            serv_req_list.append({"customer_email":customer_email, "pro_email":pro_email, "request_id":req.request_id, "service_name": service_name, "request_date":req.req_date, "close_date":req.close_date, "status":req.status})
        return jsonify({"services": service_list, "professional": prolist, "customer": customlist, "service_req":serv_req_list}), 200
    

    @app.route('/admin/create_service', methods=['POST'])
    @auth_required('token')
    @roles_required('admin')
    def create_service():
        data = request.get_json()
        if not Services.query.filter_by(service_name=data["service_name"]).first():
            new_service = Services(
                service_category=data["service_category"],
                service_name=data["service_name"].title(),
                expected_time=data["expected_time"],
                description=data["description"],
                base_price=data["base_price"]
            )
            db.session.add(new_service)
            db.session.commit()
            return jsonify({"message": "Service Created Successfully!"}), 201
        return jsonify({"message": "Service already exist"}), 400

    @app.route('/admin/update_service/<int:service_id>', methods=['PUT'])
    @auth_required('token')
    @roles_required('admin')
    def update_service(service_id):
        data = request.get_json()
        service = Services.query.get(service_id)
        
        if not service:
            return jsonify({"message": "Service not found"}), 404

        pro=Professional.query.filter_by(service_name=service.service_name).first()
        if not pro:
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
        return jsonify({"message": "Service is in use"}), 400

    @app.route('/available_services')
    def services():
        services = [service.service_name for service in Services.query.all()]
        return jsonify({"services": services})
    

    @app.route('/admin/delete/<int:service_id>', methods=['DELETE'])
    @auth_required('token')
    @roles_required('admin')
    def delete_service(service_id):
        
        service = Services.query.get(service_id)
        if Professional.query.filter_by(service_name=service.service_name).first():
            return jsonify({"message": "Service is in use"}), 400
        
        db.session.delete(service)
        db.session.commit()

        return jsonify({"message":"Record deleted successfully"}), 200

    @app.route('/admin/block_unblock_user/<int:id>', methods=["PUT"])
    @auth_required('token')
    @roles_required('admin')
    def block_unblock_user(id):

        user = User.query.get(id)
        if user and user.roles[0].name == 'customer':
            user.active = not user.active

            db.session.commit()
            return jsonify({"message": f"Customer {'unblock' if user.active else 'block' } successfully"}), 200
        return jsonify({"message": "User not found"}), 404
    

    @app.route('/admin/accept_reject_pro/<int:id>', methods=["PUT"])
    @auth_required('token')
    @roles_required('admin')
    def block_unblock_pro(id):
        user = User.query.get(id)
        pro = Professional.query.filter_by(user_id=user.id).first()
        if user and user.roles[0].name == 'professional':
            user.active = not user.active

            
            pro.status = ''
            db.session.commit()
            return jsonify({"message": f"Professional {'unblock' if user.active else 'block' } successfully"}), 200
        return jsonify({"message": "User not found"}), 404
    
    @app.route('/admin_summary', methods=['GET'])
    @auth_required('token')
    @roles_required('admin')
    def admin_summary():
        totalPro = Professional.query.count()
        pendingApprovals = Professional.query.filter_by(status='Waiting for admin approval..').count()
        blockedPro = db.session.query(User).filter(User.active == False,User.id.in_(db.session.query(Professional.user_id).filter(Professional.status != 'Waiting for admin approval..'))).count()

        totalServices=Services.query.count()
        registerServices=db.session.query(User).filter(User.active == True, User.id == Professional.user_id).count()
        vacantServices=totalServices-registerServices

        totalCustomer=Customer.query.count()
        blockedCustomer=db.session.query(User).filter(User.active == False, User.id == Customer.user_id).count()
        activeCustomer = totalCustomer-blockedCustomer

        total_Servicereq = Service_Request.query.count()
        pending_req = Service_Request.query.filter_by(status = 'Requested').count()
        pro_dismiss = Service_Request.query.filter_by(status ='Dismissed by professional').count()
        complete_req = Service_Request.query.filter_by(status = 'Closed by customer').count()
        return jsonify({"totalPro": totalPro, "pendingApproval": pendingApprovals, "blockedPro": blockedPro,
                         "totalServices":totalServices, "registerServices":registerServices, "vacantServices":vacantServices,
                         "totalCustomer":totalCustomer, "blockedCustomer":blockedCustomer, "activeCustomer":activeCustomer,
                         "totalreq":total_Servicereq, "pending_req":pending_req, "pro_dismissed":pro_dismiss, "complete_req":complete_req}), 200

    # Customer Routes
    @app.route('/register_customer', methods=['POST'])
    def register_customer():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')
        address = data.get('address')
        contact = data.get('contact')
        gender = data.get('gender')
        pincode = data.get('pincode')

        if app.security.datastore.find_user(email=email) is None:
            try:
                user = app.security.datastore.create_user(email=email, password=hash_password(password), fullname=fullname)
                role = app.security.datastore.find_role('customer')
                app.security.datastore.add_role_to_user(user, role)

                customer = Customer(user_id=user.id, address=address, contact=contact, pin_code=pincode, gender=gender)
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

        user = app.security.datastore.find_user(email=email)
        if not user:
            return jsonify({'message': 'User does not exist'}), 404 

        if verify_password(password, user.password):
            return jsonify({'token': user.get_auth_token(), 'email': user.email}), 200 
        return jsonify({'message': 'Wrong password'}), 400

    @app.route('/customer_dashboard', methods=['GET'])
    @auth_required('token')
    @roles_required('customer')
    def customer_dashboard():
        custom=Customer.query.filter_by(user_id=current_user.id).first()

        serv_req_list = []
        serv_req = Service_Request.query.filter_by(customer_id=current_user.id).all()
        for req in serv_req:
            pro_email = User.query.get(req.professional_id).email
            service_name = Services.query.get(req.service_id).service_name
            serv_req_list.append({"pro_email":pro_email, "request_id":req.request_id, "service_name": service_name, "request_date":req.req_date, "close_date":req.close_date, "schedule_date":req.schedule_date, "status":req.status})

        services_list = []
        for serv in Services.query.all():
            pro = Professional.query.filter_by(service_name = serv.service_name).first()
            
            services_list.append({"service_id":serv.service_id, "service_name":serv.service_name, "service_category":serv.service_category, "price":serv.base_price, "rating":pro.rating if pro else None, "description":serv.description})

        return jsonify({"profile":{"name": current_user.fullname, "email": current_user.email, "contact":custom.contact, "address":custom.address, "pincode":custom.pin_code},
                        "service_req":serv_req_list, "services":services_list}), 200
    

    @app.route('/request_service', methods=['POST'])
    @auth_required('token')
    @roles_required('customer')
    def request_service():
        data = request.get_json()
        service_id = data.get('service_id')
        service_name = data.get('service_name')
        pro_id = Professional.query.filter_by(service_name = service_name, status = '').first()
        if not pro_id:
            return jsonify({'message':'Professional not found'}), 404
        
        if not Service_Request.query.filter_by(service_id = service_id, customer_id = current_user.id).first():
            serve_req = Service_Request(request_id=str(uuid.uuid4())[:4], service_id=service_id, customer_id=current_user.id, professional_id=pro_id.user_id, schedule_date=dt.utcnow() + timedelta(days=2))
            db.session.add(serve_req)
            db.session.commit()

            serv_req = Service_Request.query.filter_by(customer_id=current_user.id, request_id = serve_req.request_id).first()
            pro_email = User.query.get(serv_req.professional_id).email
            service_name = Services.query.get(serv_req.service_id).service_name
            return jsonify({'message':'Request added succesfully', "pro_email":pro_email, "request_id":serv_req.request_id, "service_name": service_name, "request_date":serv_req.req_date, "close_date":serv_req.close_date, "schedule_date":serv_req.schedule_date, "request_date":serv_req.req_date,"status":serv_req.status}), 200
        return jsonify({'message':'Service request already exist'}),400

    @app.route('/cancel_request/<string:request_id>', methods=['DELETE'])
    @auth_required('token')
    @roles_required('customer')
    def cancel_request(request_id):
        if Service_Request.query.filter_by(request_id=request_id, customer_id= current_user.id).first():
            serv_req = Service_Request.query.filter_by(request_id=request_id).first()
            db.session.delete(serv_req)
            db.session.commit()
            return jsonify({'message':'Request cancelled successfully'}), 200
        return jsonify({'message':'Request not found'}), 404
    
    @app.route('/close_edit_request/<string:action>/<string:request_id>', methods=['PUT'])
    @auth_required('token')
    @roles_required('customer')
    def close_edit_request(action, request_id):
        serv_req = Service_Request.query.filter_by(request_id=request_id, customer_id =current_user.id).first()
        if serv_req:
            if action == 'close':
                serv_req.status = 'Closed by customer'
                serv_req.close_date = dt.utcnow()
                db.session.commit()
                return jsonify({'message':'Closed by customer'}), 200

            if action == 'edit':
                data=request.get_json()
                schedule_date = data.get('schedule_date')
                serv_req.schedule_date = schedule_date
                db.session.commit()
                return jsonify({'message':"New date scheduled successfully"}), 200
        
        return jsonify({'message':'Service request not found'}), 404
    
    @app.route('/pro_remarks/<string:service_name>', methods=['GET','POST'])
    @auth_required('token')
    @roles_required('customer')
    def pro_remarks(service_name):
        if request.method == 'GET':
            service = Services.query.filter_by(service_name = service_name).first()
            if service:
                return jsonify({'pro_name':User.query.filter(Professional.query.filter_by(service_name = service_name).first().user_id == User.id).first().fullname,
                                'service_name':service.service_name,
                                'pro_email':User.query.filter(Professional.query.filter_by(service_name = service_name).first().user_id == User.id).first().email,
                                'experience':Professional.query.filter_by(service_name=service_name).first().experience
                            })
            
        if request.method == 'POST':
            data = request.get_json()
            rating = data.get('rating')
            pro = Professional.query.filter_by(service_name = service_name).first()
            if pro:
                pro.rating = rating
                db.session.commit()
                return jsonify({'message':'Rating added sucessfully'}), 200
            
            return jsonify({'message':'Not found'}), 404
                

    @app.route('/search_services', methods=['GET', 'POST'])
    @auth_required('token')
    @roles_required('customer')
    def search_services():
        if request.method == 'GET': 
            services_list = []
            serv = Services.query.filter(Professional.service_name == Services.service_name).all()
            for service in serv:
                pro = Professional.query.filter_by(service_name = service.service_name).first()
                services_list.append({'service_category':service.service_category, 'service_name':service.service_name, 'rating':pro.rating, 'description':service.description, 'base_price':service.base_price})
            return jsonify({'services':services_list})    
        
        if request.method == 'POST':
    
            return 'post'       

    # Professional Routes

    @app.route('/register_professional', methods=['POST'])
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

        if not app.security.datastore.find_user(email=email):
            try:
                if Professional.query.filter_by(service_name=service_name).first():
                    return jsonify({'message': 'Professional already registered with the service'}), 400
                
                if Professional.query.filter_by(address=address).first():
                    return jsonify({'message': 'Professional already registered with the address'}), 400
                user = app.security.datastore.create_user(email=email, password=hash_password(password), fullname=fullname, active=False)
                role = app.security.datastore.find_role('professional')
                app.security.datastore.add_role_to_user(user, role)

                pro = Professional(user_id=user.id, address=address, pin_code=pincode, service_category=service_category,
                                   experience=experience, service_name=service_name)
                db.session.add(pro)
                db.session.commit()
                return jsonify({'message': 'Registered Successfully'}), 200
            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify({"message": "Some eror occured"}), 400
        return jsonify({'message': 'User already exist'}), 400

    @app.route('/login_professional', methods=['POST'])
    def login_professional():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = app.security.datastore.find_user(email=email)
        pro =''
        if not user:
            return jsonify({'message': 'User does not exist'}), 404
            
        pro=Professional.query.filter_by(user_id=user.id).first() 

        if not verify_password(password, user.password):
                return jsonify({'message': 'Wrong password'}), 400 
        
        if user.active == False and pro.status == 'Waiting for admin approval..':
                return jsonify({'message': 'Waiting for admin approval..'}), 400
        
        if user.active == False and pro.status != 'Waiting for admin approval..':
                return jsonify({'message': 'Your are rejected by admin'}), 400
        
        return jsonify({'token': user.get_auth_token(), 'email': user.email}), 200
            
        
    @app.route('/professional_dashboard', methods=['GET'])
    @auth_required('token')
    @roles_required('professional')
    def professional_dashboard():
        pro = current_user
        pro_info = Professional.query.filter_by(user_id=pro.id).first()
        pro_detail={"name": pro.fullname, "email": pro.email, "experience":pro_info.experience, "address":pro_info.address, "service_name": pro_info.service_name}

        custom_list=[]
        serv_req = Service_Request.query.filter_by(professional_id=pro.id, status = 'Requested').all()
        for req in serv_req:
            custom1=User.query.get(req.customer_id)
            custom2=Customer.query.filter_by(user_id=custom1.id).first()
            
            custom_list.append({"service_id":req.service_id, "request_id":req.request_id, "customer_name":custom1.fullname, "customer_email":custom1.email, "contact":custom2.contact, "address":custom2.address, "schedule_date":req.schedule_date})

        closed_req = []
        close_serv = Service_Request.query.filter(or_(Service_Request.status == 'Closed by customer', Service_Request.status == 'Dismissed by professional'), Service_Request.professional_id == pro.id).all()
        for req in close_serv:
            closed_req.append({"customer_name":User.query.get(req.customer_id).fullname, "service_id":req.service_id, "status":req.status, "request_id":req.request_id})

        accept_req = []
        accept_serv = Service_Request.query.filter_by(professional_id = current_user.id, status='Accepted by professional').all()
        for accept in accept_serv:
            accept_req.append({"request_id":accept.request_id, "customer_name":User.query.get(accept.customer_id).fullname, "service_id":accept.service_id, "status":accept.status})
        return jsonify({"pro_detail":pro_detail, "service_req":custom_list, "closed_req":closed_req ,"accept_req":accept_req}), 200
    
        
    
    @app.route('/serv_req/<string:action>', methods=['PUT'])
    @auth_required('token')
    @roles_required('professional')
    def req_accept_dismiss(action):

        data=request.get_json()
        print(data,action)
        req_id = data.get('req_id')

        req = Service_Request.query.filter_by(request_id=req_id).first()
        if req:
            if action == 'Accept':
                req.status = "Accepted by professional"

            if action == 'Dismiss':
                req.status = "Dismissed by professional"    

            db.session.commit()
            return jsonify({"message":"Status added successfully", "status":req.status}), 200
        return jsonify({"message":"Record not found"}), 404
