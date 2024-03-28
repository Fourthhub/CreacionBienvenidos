
import logging
import os
from weasyprint import HTML
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import azure.functions as func

app = func.FunctionApp()
import os
from weasyprint import HTML
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def enviarMail():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Documento de Prueba</title>
    </head>
    <body>
        <h1>Saludos desde WeasyPrint</h1>
        <p>Este es un ejemplo de documento PDF generado desde HTML.</p>
    </body>
    </html>
    """
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(target=pdf_bytes)
    pdf_bytes.seek(0)  # Regresa al inicio del buffer

    # Preparar el correo electrónico con SendGrid
    message = Mail(
        from_email='reservas@apartamentoscantabria.net',
        to_emails='reservas@apartamentoscantabria.net',
        subject='Aquí está tu PDF',
        html_content='<strong>Te he adjuntado el PDF generado desde HTML.</strong>'
    )

    # Adjuntar el PDF generado en memoria
    encoded_file = base64.b64encode(pdf_bytes.read()).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded_file)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName('documento_de_prueba.pdf')
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment

    # Enviar el correo electrónico
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code, response.body, response.headers)
    except Exception as e:
        print(str(e))

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    

    

    logging.info('Python timer trigger function executed.')