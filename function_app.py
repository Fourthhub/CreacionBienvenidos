import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from weasyprint import HTML
import azure.functions as func

app = func.FunctionApp()

def generate_pdf(pdf_path):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Documento de Prueba</title>
        <style>
            body { font-family: "Arial"; }
            h1 { color: #333366; }
            p { color: #666; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Saludos desde WeasyPrint</h1>
        <p>Este es un ejemplo de documento PDF generado desde HTML.</p>
    </body>
    </html>
    """
    HTML(string=html_content).write_pdf(pdf_path)

def send_email_with_attachment(attachment_path):
    sender_email = "diegoechaure@hotmail.es"
    password = "942679432"
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "reservas@apartamentoscantabria.net"
    message["Subject"] = "Hellooo"
    message.attach(MIMEText("Aqui estan los bienvenidos", "plain"))
    # Adjuntar el PDF
    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
    message.attach(part)

    # Enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

    pdf_path = "/tmp/mydocument.pdf"
    generate_pdf(pdf_path)
    send_email_with_attachment(pdf_path)

    

    logging.info('Python timer trigger function executed.')