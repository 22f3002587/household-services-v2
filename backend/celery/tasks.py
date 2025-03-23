from celery import shared_task
import time
from backend.models import * 
import flask_excel as excel
from sqlalchemy import or_
from backend.celery.mail_service import send_email

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

@shared_task(ignore_results = True)
def email_reminder():
    pending_request = Service_Request.query.filter_by(status = 'Requested').all()

    if not pending_request:
        return "No pending service request found."
    
    for request in pending_request:
        professional = User.query.filter_by(id = request.professional_id).first()

        if professional and professional.email:
            recipient = professional.email
            subject = "<h1>Reminder: Pending Service Request</h1>"
            body = f"""
                    <h3>Dear {professional.fullname},</h3>
                    <p>You have a pending service request (ID: {request.request_id}).
                    Please visit the portal to accept or reject it.

                    Best Regards,
                    Your Service Team</p>
                    """

        send_email(recipient,subject,body)
    return f"Sent {len(pending_request)} reminders successfully"