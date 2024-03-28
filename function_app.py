
import logging
import os
import base64
import requests
from io import BytesIO
from weasyprint import HTML
import azure.functions as func

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox362f74d18132446fb3275a04b3426ccb.mailgun.org/messages",
		auth=("api", "5e590bb029cdc79ceed83d3475b10659-f68a26c9-d0f10be3"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox362f74d18132446fb3275a04b3426ccb.mailgun.org>",
			"to": "diego <diegoechaure@gmail.com>",
			"subject": "Hello diego",
			"text": "Congratulations diegoewewfewefw, you just sent an email fekaaaa with Mailgun! You are truly awesome!"})

@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:

 
    enviarMail()
    
    logging.info('Python timer trigger function executed.')