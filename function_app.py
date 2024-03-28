
import logging
import os
import base64
from io import BytesIO
from weasyprint import HTML
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import azure.functions as func

app = func.FunctionApp()
def enviarMail():
    message = Mail(
        from_email='from_email@example.com',
        to_emails='to@example.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    
    logging.info('Python timer trigger function executed.')