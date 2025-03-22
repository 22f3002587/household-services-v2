from celery import shared_task
import time
from backend.models import * 
import flask_excel as excel
from sqlalchemy import or_

@shared_task(ignore_result = False)
def add(x,y):
    time.sleep(10)
    return x+y

@shared_task(ignore_result = False)
def create_csv():
    resource = Service_Request.query.filter(or_(Service_Request.status == 'Closed by customer', Service_Request.status == 'Dismissed by professional')).all()

    column_names = [column.name for column in Service_Request.__table__.columns]
    csv = excel.make_response_from_query_sets(resource, column_names=column_names, file_type ='csv')

    with open('./backend/celery/user-downloads/closed_services.csv', 'wb') as file:
        file.write(csv.data)
    return 'closed_services.csv'