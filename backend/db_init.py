from backend.models import db, Role, User
from flask import current_app as app
from flask_security import hash_password, SQLAlchemyUserDatastore

def init_db():
    with app.app_context():  
        datastore : SQLAlchemyUserDatastore=app.security.datastore  
        roles = ['admin', 'customer', 'professional']
        
        for role in roles:
            if Role.query.filter_by(name=role).first() is None:
                role_entry = Role(name=role, description=f'this is {role}')
                db.session.add(role_entry)
            db.session.commit()                
        
        if User.query.filter_by().first() is None:
            user=datastore.create_user(email="harshit@admin.com", password="admin123", fullname="Harshit")
            datastore.add_role_to_user(user, datastore.find_role('admin'))
            db.session.commit()

