
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
    to_emails='diegoechaure@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
         logging.error(f"Error en la función: {str(e)}")


    

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    
    logging.info('Python timer trigger function executed.')