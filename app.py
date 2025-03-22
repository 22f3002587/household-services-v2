from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_cors import CORS  
from backend.models import db, User, Role
from backend.config import Config
from backend.routes import create_routes
from flask_caching import Cache
from backend.celery.celery_factory import celery_init_app
import flask_excel as excel


def CreateApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    cache = Cache(app)

    excel.init_excel(app)
    CORS(app, resources={r"/*":{"origin":"http://localhost:8080"}})

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)
    
    
    with app.app_context():
        create_routes(app, cache)

    
    return app

app = CreateApp()

celery_app = celery_init_app(app)

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

if __name__ == '__main__':
    app.run() 
