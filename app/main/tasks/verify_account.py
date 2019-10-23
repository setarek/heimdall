from app.main import celery
from flask_mail import Mail, Message
from app.main import app

mail = Mail(app)


@celery.task()
def send_async_email(email_data):
    msg = Message(email_data['subject'],
                  sender='serlina.karimi72@gmail.com',
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)
