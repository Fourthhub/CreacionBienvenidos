
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
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    
    logging.info('Python timer trigger function executed.')