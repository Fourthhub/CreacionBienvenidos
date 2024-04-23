
import logging
import os
import base64
from io import BytesIO
import requests
from datetime import datetime
from weasyprint import HTML
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition,To
import azure.functions as func

URL_HOSTAWAY_TOKEN = "https://api.hostaway.com/v1/accessTokens"
value_mapping = {
    "Rocio": "R",
    "Alojamientos": "A"
}
app = func.FunctionApp()
def enviarMail(reservas,token):
    base_html = """<!DOCTYPE html><html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en" style="box-sizing:border-box"><head style="box-sizing:border-box"><title style="box-sizing:border-box"></title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" style="box-sizing:border-box"><meta name="viewport" content="width=device-width,initial-scale=1" style="box-sizing:border-box"><!--[if mso]><xml><o:officedocumentsettings><o:pixelsperinch>96</o:pixelsperinch><o:allowpng></o:officedocumentsettings></xml><![endif]--><!--[if !mso]>
					<!--><!--
					<![endif]--></head><body style="background-color:#fff;margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none;box-sizing:border-box"><table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:10px;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:10px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:15px;padding-right:15px;width:100%;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:213px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="213" height="auto"></div></div></td></tr></table><table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:5px;padding-left:15px;padding-right:15px;padding-top:5px;text-align:center;width:100%;box-sizing:border-box"><h1 style="margin:0;color:#393939;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:32px;font-weight:700;letter-spacing:-1px;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:38.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Apartamento}<br style="box-sizing:border-box"></span></h1></td></tr></table><table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;padding-right:10px;box-sizing:border-box"><div class="alignment" align="center" style="box-sizing:border-box"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="divider_inner" style="font-size:1px;line-height:1px;border-top:2px solid #3d3d3d;box-sizing:border-box"><span style="box-sizing:border-box">&#8202;</span></td></tr></table></div></td></tr></table><table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><h3 style="margin:0;color:#3e3e3e;direction:ltr;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;font-size:22px;font-weight:400;letter-spacing:normal;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:26.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Nombre}</span></h3></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#d4d4d4;border-bottom:17px solid transparent;border-left:17px solid transparent;border-radius:30px;border-right:17px solid transparent;border-top:17px solid transparent;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><u style="box-sizing:border-box"><span style="font-size:16px;box-sizing:border-box"><strong style="box-sizing:border-box">PAGOS</strong></span></u></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">Total Estancia:</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">Realizado:</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:'Trebuchet MS',Tahoma,sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#080808;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">A pagar:</span></p></div></div></td></tr></table></td><td class="column column-2" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#555;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">&nbsp;</span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Total_estancia}</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Pagado}</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{restante}</span></p></div></div></td></tr></table></td><td class="column column-3" width="50%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box"><u style="box-sizing:border-box"><strong style="box-sizing:border-box">DETALLES</strong></u></span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📍 {address}</p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📆 &nbsp;Del {fechachekin} al {fechacheckout}</p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">👤 &nbsp;{numero_de_huespeds} huéspedes</p></div></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#101112;direction:ltr;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;font-size:9px;font-weight:400;letter-spacing:0;line-height:120%;text-align:center;mso-line-height-alt:10.799999999999999px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit"><em style="box-sizing:border-box">----<strong style="box-sizing:border-box">{facturacion}</strong>----</em></p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;color:#000;border-radius:2px;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:20px;padding-right:10px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:70.875px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="70.875" alt="Headset Icon" title="Headset Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-right:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Al momento de completar el check-in se realizará una<strong style="box-sizing:border-box"> retención bancaria &nbsp;de 150€ </strong>como garantía de posibles deterioros de la vivienda, perdida de llaves, retraso en la salida ó limpieza final. Esta retención se liberará tras la revisión del alojamiento posterior al check-out.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:78.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="78.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben<strong style="box-sizing:border-box"> respetar un horario de silencio </strong>de 23:00 a 08:00 horas, mantener las áreas comunes limpias y ordenadas, y tratar a todos con respeto y cortesía. El incumplimiento de estas normas puede resultar en medidas correctivas, incluido el desalojo sin reembolso.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-6" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-left:20px;padding-right:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:78.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="78.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">&nbsp;</p><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">La estancia de<strong style="box-sizing:border-box"> más personas de las acordadas </strong>, o de animales de compañía no especificados en la reserva, conllevará la expulsión inmediata de la propiedad.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">&nbsp;</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:30px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:70.875px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="70.875" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben informar al anfitrión de<strong style="box-sizing:border-box"> cualquier daño </strong>o <strong style="box-sizing:border-box">desperfecto </strong>en la propiedad dentro de las 48 horas siguientes a su llegada. La omisión de este reporte puede conllevar a que el huésped sea considerado responsable de los daños no declarados.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-8" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;width:100%;padding-right:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:76.25px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="76.25" alt="Notes Icon" title="Notes Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit"><strong style="box-sizing:border-box">Apartamentos Cantabria no se hará responsable por:</strong></p></div></td></tr></table><table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;font-weight:400;letter-spacing:0;line-height:120%;text-align:justify;mso-line-height-alt:14.399999999999999px;box-sizing:border-box"><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">I. Negligencias o fallos de servicios atribuibles a terceros.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">II. Mal funcionamiento de piscinas, áreas recreativas o instalaciones deportivas, cuyo uso será bajo la responsabilidad del huésped.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">III. Robos o pérdidas sufridas por los huéspedes en la propiedad.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">IV. Daños personales o materiales ocasionados por fuerzas mayores o situaciones imprevistas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">V. Molestias por ruidos de obras cercanas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">VI. Cortes en el suministro de agua, gas o electricidad por parte de proveedores.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">VII. Retrasos en las reparaciones de electrodomésticos y calderas por servicios técnicos oficiales.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></body></html>"""

    German_html="""<!DOCTYPE html>
    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="es-ES" style="box-sizing: border-box;">

    <head style="box-sizing: border-box;">
        <title style="box-sizing: border-box;"></title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" style="box-sizing: border-box;">
        <meta name="viewport" content="width=device-width, initial-scale=1.0" style="box-sizing: border-box;"><!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]--><!--[if !mso]><!-->
        <!--<![endif]-->
        
    </head>

    <body style="background-color: #ffffff;margin: 0;padding: 0;-webkit-text-size-adjust: none;text-size-adjust: none;box-sizing: border-box;">
        <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #ffffff;box-sizing: border-box;">
            <tbody style="box-sizing: border-box;">
                <tr style="box-sizing: border-box;">
                    <td style="box-sizing: border-box;">
                        <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 10px;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="100%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 20px;padding-right: 20px;padding-top: 10px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 15px;padding-right: 15px;width: 100%;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 213px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="213" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 5px;padding-left: 15px;padding-right: 15px;padding-top: 5px;text-align: center;width: 100%;box-sizing: border-box;">
                                                                    <h1 style="margin: 0;color: #393939;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 32px;font-weight: 700;letter-spacing: -1px;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 38.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Apartamento}<br style="box-sizing: border-box;"></span></h1>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-left: 10px;padding-right: 10px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="box-sizing: border-box;">
                                                                        <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                                            <tr style="box-sizing: border-box;">
                                                                                <td class="divider_inner" style="font-size: 1px;line-height: 1px;border-top: 2px solid #3d3d3d;box-sizing: border-box;"><span style="box-sizing: border-box;">&#8202;</span></td>
                                                                            </tr>
                                                                        </table>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <h3 style="margin: 0;color: #3e3e3e;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 22px;font-weight: 400;letter-spacing: normal;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 26.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Nombre}</span></h3>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #d4d4d4;border-bottom: 17px solid transparent;border-left: 17px solid transparent;border-radius: 30px;border-right: 17px solid transparent;border-top: 17px solid transparent;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><u style="box-sizing: border-box;"><span style="font-size: 16px;box-sizing: border-box;"><strong style="box-sizing: border-box;">PAYMENTS</strong></span></u></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">Gesamtaufenthalt:</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">Bezahlt:</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: 'Trebuchet MS', Tahoma, sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #080808;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">Fällig heute:</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 20px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #555555;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">&nbsp;</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Total_estancia}</span></p>
                                                                            <p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Pagado}</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{restante}</span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-3" width="50%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;"><u style="box-sizing: border-box;"><strong style="box-sizing: border-box;">DETAILS</strong></u></span></p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📍 {address}</p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📆 &nbsp;From {fechachekin} to {fechacheckout}</p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
                                                                    <div style="font-family: sans-serif;box-sizing: border-box;">
                                                                        <div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
                                                                            <p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">👤 &nbsp;{numero_de_huespeds}</p>
                                                                        </div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="100%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <div style="color: #101112;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 9px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: center;mso-line-height-alt: 10.799999999999999px;box-sizing: border-box;">
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;"><em style="box-sizing: border-box;">----<strong style="box-sizing: border-box;">{facturacion}</strong>----</em></p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #ffffff;color: #000000;border-radius: 2px;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 20px;padding-right: 10px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Headset Icon" title="Headset Icon" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-right: 10px;box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;">Zum Zeitpunkt des Check-Ins wird eine Bankrückstellung von 150€ als Garantie für mögliche Schäden am Eigentum, Verlust von Schlüsseln, Verspätung bei der Abreise oder Endreinigung vorgenommen. Diese Rückstellung wird nach der Inspektion der Unterkunft nach dem Check-out freigegeben.</p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 20px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;">Gäste müssen eine Ruhezeit von 23:00 bis 08:00 Uhr respektieren, Gemeinschaftsbereiche sauber und ordentlich halten und jeden mit Respekt und Höflichkeit behandeln. Die Nichteinhaltung dieser Regeln kann zu korrektiven Maßnahmen führen, einschließlich der Räumung ohne Rückerstattung.</p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-6" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-left: 20px;padding-right: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
                                                                        <p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
                                                                        <p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">Der Aufenthalt von mehr Personen als vereinbart oder von Haustieren, die nicht in der Reservierung angegeben sind, führt zur sofortigen Ausweisung aus dem Eigentum.</p>
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 30px;padding-left: 20px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;">Gäste müssen den Gastgeber innerhalb von 48 Stunden nach ihrer Ankunft über etwaige Schäden oder Mängel am Eigentum informieren. Die Unterlassung dieser Meldung kann dazu führen, dass der Gast für die nicht deklarierten Schäden als verantwortlich angesehen wird.</p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="row row-8" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                            <tbody style="box-sizing: border-box;">
                                <tr style="box-sizing: border-box;">
                                    <td style="box-sizing: border-box;">
                                        <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
                                            <tbody style="box-sizing: border-box;">
                                                <tr style="box-sizing: border-box;">
                                                    <td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 25px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-left: 10px;width: 100%;padding-right: 0px;box-sizing: border-box;">
                                                                    <div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
                                                                        <div style="max-width: 76.25px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="76.25" alt="Notes Icon" title="Notes Icon" height="auto"></div>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                    <td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
                                                        <table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="padding-bottom: 10px;box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;"><strong style="box-sizing: border-box;">Apartamentos Cantabria will not be responsible of:</strong></p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        <table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
                                                            <tr style="box-sizing: border-box;">
                                                                <td class="pad" style="box-sizing: border-box;">
                                                                    <div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 12px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: justify;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;">
                                                                        <p style="margin: 0;margin-bottom: 1px;box-sizing: border-box;line-height: inherit;">I. Fahrlässigkeit oder Dienstleistungsausfälle, die Dritten zuzuschreiben sind.</p>
                                                                        <p style="margin: 0;margin-bottom: 1px;box-sizing: border-box;line-height: inherit;">II. Fehlfunktion von Schwimmbädern, Erholungsgebieten oder Sporteinrichtungen, deren Nutzung &nbsp;in der Verantwortung des Gastes liegt.</p>
                                                                        <p style="margin: 0;margin-bottom: 1px;box-sizing: border-box;line-height: inherit;">III. Diebstähle oder Verluste, die Gäste auf dem Eigentum erleiden.</p>
                                                                        <p style="margin: 0;margin-bottom: 1px;box-sizing: border-box;line-height: inherit;">IV. Persönliche oder materielle Schäden, die durch höhere Gewalt oder unvorhergesehene Situationen verursacht wurden. V. Unannehmlichkeiten durch Lärm von nahegelegenen Arbeiten. VI. Unterbrechungen der Versorgung mit Wasser, Gas oder Strom durch Anbieter.</p>
                                                                        <p style="margin: 0;box-sizing: border-box;line-height: inherit;">VII. Verzögerungen bei der Reparatur von Geräten und Kesseln durch offizielle technische Dienste.</p>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table><!-- End -->
    </body>

    </html>"""

    english_html="""<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="es-ES" style="box-sizing: border-box;">

<head style="box-sizing: border-box;">
	<title style="box-sizing: border-box;"></title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" style="box-sizing: border-box;">
	<meta name="viewport" content="width=device-width, initial-scale=1.0" style="box-sizing: border-box;"><!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]--><!--[if !mso]><!-->
	<!--<![endif]-->
	
</head>

<body style="background-color: #ffffff;margin: 0;padding: 0;-webkit-text-size-adjust: none;text-size-adjust: none;box-sizing: border-box;">
	<table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #ffffff;box-sizing: border-box;">
		<tbody style="box-sizing: border-box;">
			<tr style="box-sizing: border-box;">
				<td style="box-sizing: border-box;">
					<table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 10px;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 20px;padding-right: 20px;padding-top: 10px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 15px;padding-right: 15px;width: 100%;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 213px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="213" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
													<table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 5px;padding-left: 15px;padding-right: 15px;padding-top: 5px;text-align: center;width: 100%;box-sizing: border-box;">
																<h1 style="margin: 0;color: #393939;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 32px;font-weight: 700;letter-spacing: -1px;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 38.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Apartamento}<br style="box-sizing: border-box;"></span></h1>
															</td>
														</tr>
													</table>
													<table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-left: 10px;padding-right: 10px;box-sizing: border-box;">
																<div class="alignment" align="center" style="box-sizing: border-box;">
																	<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
																		<tr style="box-sizing: border-box;">
																			<td class="divider_inner" style="font-size: 1px;line-height: 1px;border-top: 2px solid #3d3d3d;box-sizing: border-box;"><span style="box-sizing: border-box;">&#8202;</span></td>
																		</tr>
																	</table>
																</div>
															</td>
														</tr>
													</table>
													<table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<h3 style="margin: 0;color: #3e3e3e;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 22px;font-weight: 400;letter-spacing: normal;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 26.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Nombre}</span></h3>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #d4d4d4;border-bottom: 17px solid transparent;border-left: 17px solid transparent;border-radius: 30px;border-right: 17px solid transparent;border-top: 17px solid transparent;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><u style="box-sizing: border-box;"><span style="font-size: 16px;box-sizing: border-box;"><strong style="box-sizing: border-box;">PAYMENTS</strong></span></u></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">Total Stay:</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">Paid</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: 'Trebuchet MS', Tahoma, sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #080808;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">Due Today:</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 20px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #555555;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">&nbsp;</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Total_estancia}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Pagado}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{restante}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-3" width="50%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;"><u style="box-sizing: border-box;"><strong style="box-sizing: border-box;">DETAILS</strong></u></span></p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📍 {address}</p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📆 &nbsp;From {fechachekin} to {fechacheckout}</p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">👤 &nbsp;{numero_de_huespeds}</p>
																	</div>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #101112;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 9px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: center;mso-line-height-alt: 10.799999999999999px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;"><em style="box-sizing: border-box;">----<strong style="box-sizing: border-box;">{facturacion}</strong>----</em></p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #ffffff;color: #000000;border-radius: 2px;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 20px;padding-right: 10px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Headset Icon" title="Headset Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-right: 10px;box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Upon completing the check-in, a bank hold of €150 will be made as a guarantee for possible damage to the dwelling, loss of keys, delay in departure, or final cleaning. This hold will be released after the accommodation is reviewed following check-out.</p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 20px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Guests must observe a quiet time from 11:00 PM to 8:00 AM, keep common areas clean and orderly, and treat everyone with respect and courtesy. Failure to comply with these rules may result in corrective measures, including eviction without a refund.</p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-6" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-left: 20px;padding-right: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
																	<p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">The stay of more people than agreed upon, or of pets not specified in the reservation, will lead to immediate expulsion from the property.</p>
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 30px;padding-left: 20px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Guests must inform the host of any damage or defect in the property within 48 hours of their arrival. Failure to report this may lead to the guest being considered responsible for undeclared damages.</p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table class="row row-8" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
						<tbody style="box-sizing: border-box;">
							<tr style="box-sizing: border-box;">
								<td style="box-sizing: border-box;">
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-radius: 0;color: #000000;width: 750px;margin: 0 auto;box-sizing: border-box;" width="750">
										<tbody style="box-sizing: border-box;">
											<tr style="box-sizing: border-box;">
												<td class="column column-1" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 10px;padding-left: 25px;padding-right: 10px;padding-top: 10px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-left: 10px;width: 100%;padding-right: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 76.25px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="76.25" alt="Notes Icon" title="Notes Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;"><strong style="box-sizing: border-box;">Apartamentos Cantabria will not be responsible of:</strong></p>
																</div>
															</td>
														</tr>
													</table>
													<table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 12px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: justify;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">I. Negligence or service failures attributable to third parties.<br style="box-sizing: border-box;">II. Malfunction of swimming pools, recreational areas, or sports facilities, the use of which will be under the responsibility of the guest.<br style="box-sizing: border-box;">III. Thefts or losses suffered by guests on the property.<br style="box-sizing: border-box;">IV. Personal or material damage caused by force majeure or unforeseen situations.<br style="box-sizing: border-box;">V. Disturbances due to noise from nearby construction.<br style="box-sizing: border-box;">VI. Cuts in the supply of water, gas, or electricity by suppliers.<br style="box-sizing: border-box;">VII. Delays in the repair of appliances and boilers by official technical services.</p>
																</div>
															</td>
														</tr>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table><!-- End -->
</body>

</html>"""
    # Generar el HTML completo con 3 páginas
    full_html = "<html><head><title>Documento Multi-página</title></head><body>"
    
    for reserva in reservas["result"]:
        html = base_html
        if reserva["status"] != "modified" and reserva["status"] != "new":
            continue
        if reserva["localeForMessaging"] == "de":
            html=German_html
        if reserva["localeForMessaging"] == "en":
            html=english_html
        if reserva["localeForMessaging"] == "fr":
            html=German_html
        listingID = reserva["listingMapId"]
        address,serieFact = direccionListing(token, listingID)  # Obtener la dirección una sola vez por reserva
        
        total= reserva["totalPrice"]
        remin= reserva["remainingBalance"]
        pagado=round(total - remin, 2)
        # Ejecutar dos veces por cada reserva
        for _ in range(2):
            full_html += html.format(
                Apartamento=reserva["listingName"],
                Nombre=reserva["guestName"],
                Total_estancia=str(total) + " " + reserva["currency"],
                Pagado=str(pagado)+ " " + reserva["currency"],  # Asegúrate de definir cómo obtener este valor
                restante=str(remin) + " " + reserva["currency"],
                address=address,  # Usar la dirección obtenida previamente
                fechachekin=reserva["arrivalDate"],
                fechacheckout=reserva["departureDate"],
                numero_de_huespeds=str(reserva["numberOfGuests"]),
                facturacion=serieFact
            ) + "<div style='page-break-after: always;'></div>"
        full_html += "</body></html>"
    # Generar el PDF desde HTML y mantenerlo en memoria
    
    encoded_file = base64.b64encode(full_html.encode()).decode()
    

    # Crear el mensaje de correo con SendGrid
    message = Mail(
        from_email='reservas@apartamentoscantabria.net',
        to_emails=[
        To('diegoechaure@gmail.com'),
        To('reservas@apartamentoscantabria.net'),
    ],
        subject='Chekins de hoy',
        html_content='<strong>Los bienvenidos de hoy en isla</strong>'
    )

    # Adjuntar el PDF codificado
    attachment = Attachment()
    attachment.file_content = FileContent(encoded_file)
    attachment.file_type = FileType('text/html')
    attachment.file_name = FileName('bienvenidos.html')
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment

    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
         logging.error(f"Error en la función: {str(e)}")

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

def remainingBalance(token,idReserva):
    url= f"https://api.hostaway.com/v1/guestPayments/charges?reservationId={idReserva}"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }
    response = requests.get(url, headers=headers)
    data = response.json()['result']
    pagado=0
    for charge in data:
        if charge['status']=="paid":
            pagado+=charge['amount']
    return pagado

@app.function_name(name="crecionBienvenido")
@app.schedule(schedule="0 0 8 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:
    token = obtener_acceso_hostaway()
    hoy = datetime.now().strftime('%Y-%m-%d')
    reservas= reservasHoy(hoy,hoy,token)
    enviarMail(reservas,token)
    logging.info('Python timer trigger function executed.')