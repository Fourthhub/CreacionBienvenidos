
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
        from_email='reservas@apartamentoscantabria.net',
        to_emails='reservas@apartamentoscantabria.net',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    

    

    logging.info('Python timer trigger function executed.')