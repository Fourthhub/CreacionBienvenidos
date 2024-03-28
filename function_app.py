
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
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Documento PDF</title>
    </head>
    <body>
        <h1>Este es un PDF generado desde HTML</h1>
        <p>Este PDF ha sido generado y enviado usando WeasyPrint y SendGrid.</p>
    </body>
    </html>
    """

    # Generar el PDF desde HTML y mantenerlo en memoria
    pdf_bytes_io = BytesIO()
    HTML(string=html_content).write_pdf(target=pdf_bytes_io)
    pdf_bytes_io.seek(0)  # Regresar al inicio del stream

    # Codificar el PDF en memoria a base64
    encoded_pdf = base64.b64encode(pdf_bytes_io.getvalue()).decode()

    # Crear el mensaje de correo con SendGrid
    message = Mail(
        from_email='reservas@apartamentoscantabria.net',
        to_emails='diegoechaure@gmail.com',
        subject='PDF generado desde HTML',
        html_content='<strong>Adjunto encontrarás el PDF generado......</strong>'
    )

    # Adjuntar el PDF codificado
    attachment = Attachment()
    attachment.file_content = FileContent(encoded_pdf)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName('documento_generado.pdf')
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment

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