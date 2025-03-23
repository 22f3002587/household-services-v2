from celery import shared_task
import time
from backend.models import * 
import flask_excel as excel
from sqlalchemy import or_
from backend.celery.mail_service import send_email
from flask import render_template
from datetime import datetime as dt

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
            subject = "Reminder: Pending Service Request"
            body = f"""
                    <h1>Dear {professional.fullname},</h1><br>
                    <p>You have a pending service request (ID: {request.request_id}).
                    Please visit the portal to accept or reject it.</p><br><br>

                    <strong>Best Regards,
                    Your Service Team</strong>
                    """

        send_email(recipient,subject,body)
    return f"Sent {len(pending_request)} reminders successfully"


@shared_task(ignore_task = True)
def monthly_reminder():
    customer = User.query.join(Customer).join(User.roles).filter(
        Role.name == 'customer',
        Service_Request.customer_id == User.id,
        Service_Request.status.in_(['Closed by customer', 'Dismissed by professional'])
    ).distinct().all()

    sent_count = 0
    for custom in customer:
        request_count = Service_Request.query.filter_by(customer_id = custom.id).count()
        closed_count = Service_Request.query.filter(or_(Service_Request.status == 'Closed by customer', Service_Request.status == 'Dismissed by professional')).count()

        services = Service_Request.query.filter_by(customer_id = custom.id).all()
        service_req_data = [{
            "service_category":Services.query.filter_by(service_id=record.service_id).first().service_category,
            "service_name":Services.query.filter_by(service_id=record.service_id).first().service_name,
            "status": record.status,
            "req_date":record.req_date.strftime("%d-%m-%Y"),
            "closed_date":record.close_date.strftime("%d-%m-%Y") if record.close_date else 'N/A',
        } 
        for record in services]

        html_content = render_template('mail.html',
                                        customer_name = custom.fullname,
                                        requested_count = request_count,
                                        closed_count = closed_count,
                                        services = service_req_data)
        
        subject = f"Monthly Activity Report - {dt.now().strftime('%B %Y')}"
        send_email(custom.email, subject, html_content)
        sent_count +=1

    return f"Sent {sent_count} monthly report successfully"
    