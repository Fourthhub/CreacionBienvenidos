
import logging
import os
import base64
from io import BytesIO
import requests
from datetime import datetime
from weasyprint import HTML
from mailersend import emails
import azure.functions as func

URL_HOSTAWAY_TOKEN = "https://api.hostaway.com/v1/accessTokens"
value_mapping = {
    "Rocio": "R",
    "Alojamientos": "A"
}
app = func.FunctionApp()
def enviarMail(reservas,token):
    base_html = ""

    # Generar el HTML completo con 3 páginas
    full_html_I = "<html><head><title>Documento Multi-página I</title></head><body>"
    full_html_S = "<html><head><title>Documento Multi-página S</title></head><body>"

    for reserva in reservas["result"]:
        if reserva["status"] != "modified" and reserva["status"] != "new":
            continue

        # Seleccionar la plantilla HTML según el idioma del mensaje
        if reserva["localeForMessaging"] == "de":
            html = German_html
            huespedes = " Gäste"
        elif reserva["localeForMessaging"] == "en":
            html = english_html
            huespedes = " guests"
        elif reserva["localeForMessaging"] == "fr":
            html = french_html
            huespedes = " les hôtes"
        else:
            html = base_html
            huespedes = " huéspedes"

        listingID = reserva["listingMapId"]
        address, serieFact = direccionListing(token, listingID)  # Obtener la dirección una sola vez por reserva

        total = reserva["totalPrice"]
        remin = reserva["remainingBalance"]
        pagado = round(total - remin, 2)

        # Ejecutar dos veces por cada reserva
        if hayMascota(token, reserva["id"]):
            huespedes += """<p style="font-size: 16px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">""" + "+ 🐶</p>"

        huesped_mascota = str(reserva["numberOfGuests"]) + huespedes
        for _ in range(2):
            formatted_html = html.format(
                Apartamento=reserva["listingName"],
                Nombre=reserva["guestName"],
                Total_estancia=str(total) + " " + reserva["currency"],
                Pagado=str(pagado) + " " + reserva["currency"],  # Asegúrate de definir cómo obtener este valor
                restante=str(round(remin, 2)) + " " + reserva["currency"],
                address=address,  # Usar la dirección obtenida previamente
                fechachekin=reserva["arrivalDate"],
                fechacheckout=reserva["departureDate"],
                numero_de_huespeds=huesped_mascota,
                facturacion=serieFact
            ) + "<div style='page-break-after: always;'></div>"

            if reserva["listingName"].startswith('I'):
                full_html_I += formatted_html
            elif reserva["listingName"].startswith('S'):
                full_html_S += formatted_html

    full_html_I += "</body></html>"
    full_html_S += "</body></html>"

    # Codificar los archivos HTML en base64
    encoded_file_I = base64.b64encode(full_html_I.encode()).decode()
    encoded_file_S = base64.b64encode(full_html_S.encode()).decode()

    # Inicializar MailerSend con tu token
    mailer = emails.Emails(api_key='mlsn.dea18ac7abd367152b71e2871d6b6ef9ba3d473b89d2a3b6f46c9735a43f5b2a')

    mail_data = {
        "from": {
            "email": "reservas@apartamentoscantabria.net",
            "name": "Apartamentos Cantabria"
        },
        "to": [
            {"email": "diegoechaure@gmail.com", "name": "Diego"},
            {"email": "reservas@apartamentoscantabria.net", "name": "Reservas"}
        ],
        "subject": "📋🖨️ Chekins 🖨️📋",
        "text": "Los bienvenidos de hoy",
        "html": "<strong>Los bienvenidos de hoy</strong>",
        "attachments": [
            {
                "content": encoded_file_I,
                "filename": "ISLA.html",
                "type": "text/html",
                "disposition": "attachment"
            },
            {
                "content": encoded_file_S,
                "filename": "SOMO.html",
                "type": "text/html",
                "disposition": "attachment"
            }
        ]
    }

    try:
        response = mailer.send(mail_data)
        print(response.status_code)
        print(response.json())
    except Exception as e:
        logging.error(f"Error enviando correo con MailerSend: {str(e)}")

def obtener_acceso_hostaway():
    try:
        payload = {
            "grant_type": "client_credentials",
            "client_id": "81585",
            "client_secret": "0e3c059dceb6ec1e9ec6d5c6cf4030d9c9b6e5b83d3a70d177cf66838694db5f",
            "scope": "general"
        }
        headers = {'Content-type': "application/x-www-form-urlencoded", 'Cache-control': "no-cache"}
        response = requests.post(URL_HOSTAWAY_TOKEN, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.RequestException as e:
        logging.error(f"Error al obtener el token de acceso: {str(e)}")
        raise

def reservasHoy(arrivalStartDate, arrivalEndDate,token):
    
    url = f"https://api.hostaway.com/v1/reservations?arrivalStartDate={arrivalStartDate}&arrivalEndDate={arrivalEndDate}&includeResources=1&includePayments=1" 

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
    except Exception as e:
        raise SyntaxError(f"Error al procesar la reserva: {e}")
    return data

def direccionListing(token,listingId):
    url = f"https://api.hostaway.com/v1/listings/{listingId}?includeResources=1" 

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    serie="A"
    for field in data['result']["customFieldValues"]:
        if field["customFieldId"]==57829:
            mapped_value = value_mapping.get(field["value"], "A")  # Default a "A" si el valor no se encuentra en el mapeo
            serie = mapped_value

    return data['result']["address"],serie

def hayMascota(token,idReserva):
    url= f"https://api.hostaway.com/v1/financeField/{idReserva}"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }
    response = requests.get(url, headers=headers)
    data = response.json()['result']
    
    for element in data:
        if element['name']=="petFee":
            return True
    return False

@app.function_name(name="crecionBienvenido")
@app.schedule(schedule="0 0 8 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:
    token = obtener_acceso_hostaway()
    hoy = datetime.now().strftime('%Y-%m-%d')
    reservas= reservasHoy(hoy,hoy,token)
    enviarMail(reservas,token)
    logging.info('Python timer trigger function executed.')