
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
					<![endif]--></head><body style="background-color:#fff;margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none;box-sizing:border-box"><table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:10px;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:10px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:15px;padding-right:15px;width:100%;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:213px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="213" height="auto"></div></div></td></tr></table><table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:5px;padding-left:15px;padding-right:15px;padding-top:5px;text-align:center;width:100%;box-sizing:border-box"><h1 style="margin:0;color:#393939;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:32px;font-weight:700;letter-spacing:-1px;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:38.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Apartamento}<br style="box-sizing:border-box"></span></h1></td></tr></table><table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;padding-right:10px;box-sizing:border-box"><div class="alignment" align="center" style="box-sizing:border-box"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="divider_inner" style="font-size:1px;line-height:1px;border-top:2px solid #3d3d3d;box-sizing:border-box"><span style="box-sizing:border-box">&#8202;</span></td></tr></table></div></td></tr></table><table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><h3 style="margin:0;color:#3e3e3e;direction:ltr;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;font-size:22px;font-weight:400;letter-spacing:normal;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:26.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Nombre}</span></h3></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#d4d4d4;border-bottom:17px solid transparent;border-left:17px solid transparent;border-radius:30px;border-right:17px solid transparent;border-top:17px solid transparent;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><u style="box-sizing:border-box"><span style="font-size:16px;box-sizing:border-box"><strong style="box-sizing:border-box">PAGOS</strong></span></u></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">Total Estancia:</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">Realizado:</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:'Trebuchet MS',Tahoma,sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#080808;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">A pagar:</span></p></div></div></td></tr></table></td><td class="column column-2" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#555;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">&nbsp;</span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Total_estancia}</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Pagado}</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{restante}</span></p></div></div></td></tr></table></td><td class="column column-3" width="50%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box"><u style="box-sizing:border-box"><strong style="box-sizing:border-box">DETALLES</strong></u></span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📍 {address}</p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📆 &nbsp;Del {fechachekin} al {fechacheckout}</p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">👤 &nbsp;{numero_de_huespeds}</p></div></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#101112;direction:ltr;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;font-size:9px;font-weight:400;letter-spacing:0;line-height:120%;text-align:center;mso-line-height-alt:10.799999999999999px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit"><em style="box-sizing:border-box">----<strong style="box-sizing:border-box">{facturacion}</strong>----</em></p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;color:#000;border-radius:2px;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:20px;padding-right:10px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:70.875px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="70.875" alt="Headset Icon" title="Headset Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-right:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Al momento de completar el check-in se realizará una<strong style="box-sizing:border-box"> retención bancaria &nbsp;de 150€ </strong>como garantía de posibles deterioros de la vivienda, perdida de llaves, retraso en la salida ó limpieza final. Esta retención se liberará tras la revisión del alojamiento posterior al check-out.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:78.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="78.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben<strong style="box-sizing:border-box"> respetar un horario de silencio </strong>de 23:00 a 08:00 horas, mantener las áreas comunes limpias y ordenadas, y tratar a todos con respeto y cortesía. El incumplimiento de estas normas puede resultar en medidas correctivas, incluido el desalojo sin reembolso.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-6" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-left:20px;padding-right:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:78.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="78.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">&nbsp;</p><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">La estancia de<strong style="box-sizing:border-box"> más personas de las acordadas </strong>, o de animales de compañía no especificados en la reserva, conllevará la expulsión inmediata de la propiedad.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">&nbsp;</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:30px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:70.875px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="70.875" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben informar al anfitrión de<strong style="box-sizing:border-box"> cualquier daño </strong>o <strong style="box-sizing:border-box">desperfecto </strong>en la propiedad dentro de las 48 horas siguientes a su llegada. La omisión de este reporte puede conllevar a que el huésped sea considerado responsable de los daños no declarados.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-8" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:750px;margin:0 auto;box-sizing:border-box" width="750"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;width:100%;padding-right:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:76.25px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="76.25" alt="Notes Icon" title="Notes Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit"><strong style="box-sizing:border-box">Apartamentos Cantabria no se hará responsable por:</strong></p></div></td></tr></table><table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;font-weight:400;letter-spacing:0;line-height:120%;text-align:justify;mso-line-height-alt:14.399999999999999px;box-sizing:border-box"><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">I. Negligencias o fallos de servicios atribuibles a terceros.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">II. Mal funcionamiento de piscinas, áreas recreativas o instalaciones deportivas, cuyo uso será bajo la responsabilidad del huésped.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">III. Robos o pérdidas sufridas por los huéspedes en la propiedad.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">IV. Daños personales o materiales ocasionados por fuerzas mayores o situaciones imprevistas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">V. Molestias por ruidos de obras cercanas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">VI. Cortes en el suministro de agua, gas o electricidad por parte de proveedores.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">VII. Retrasos en las reparaciones de electrodomésticos y calderas por servicios técnicos oficiales.</p></div></td></tr></table></td></tr></tbody></table>	<table class="row row-9" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; width: 750px; margin: 0 auto;" width="750">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; text-align: center;">
														<tr>
															<td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
																<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
																	<tr>
																		<td class="alignment" style="vertical-align: middle; text-align: center;"><!--[if vml]><table align="center" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																			<!--[if !vml]><!-->
																			<table class="icons-inner" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;" cellpadding="0" cellspacing="0" role="presentation"><!--<![endif]-->
																				<tr>
																					<td style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: undefined; color: #1e0e4b; vertical-align: middle; letter-spacing: undefined; text-align: center;"><a href="http://designedwithbeefree.com/" target="_blank" style="color: #1e0e4b; text-decoration: none;">+34 942679435</a></td>
																				</tr>
																			</table>
																		</td>
																	</tr>
																</table>
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
					</table></td></tr></tbody></table></td></tr></tbody></table></body></html>"""
    french_html="""<!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="es-ES" style="box-sizing: border-box;"><head style="box-sizing: border-box;">
	<title style="box-sizing: border-box;"></title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" style="box-sizing: border-box;">
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 15px;padding-right: 15px;width: 100%;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 190px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="190" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 5px;padding-left: 15px;padding-right: 15px;padding-top: 5px;text-align: center;width: 100%;box-sizing: border-box;">
																<h1 style="margin: 0;color: #393939;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 32px;font-weight: 700;letter-spacing: -1px;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 38.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Apartamento}<br style="box-sizing: border-box;"></span></h1>
															</td>
														</tr>
													</tbody></table>
													<table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-left: 10px;padding-right: 10px;box-sizing: border-box;">
																<div class="alignment" align="center" style="box-sizing: border-box;">
																	<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
																		<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
																			<td class="divider_inner" style="font-size: 1px;line-height: 1px;border-top: 2px solid #3d3d3d;box-sizing: border-box;"><span style="box-sizing: border-box;"> </span></td>
																		</tr>
																	</tbody></table>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<h3 style="margin: 0;color: #3e3e3e;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 22px;font-weight: 400;letter-spacing: normal;line-height: 120%;text-align: center;margin-top: 0;margin-bottom: 0;mso-line-height-alt: 26.4px;box-sizing: border-box;"><span class="tinyMce-placeholder" style="box-sizing: border-box;">{Nombre}</span></h3>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><u style="box-sizing: border-box;"><span style="font-size: 16px;box-sizing: border-box;"><strong style="box-sizing: border-box;">PAIEMENTS</strong></span></u></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">total du séjour</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">Payé:</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 50px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: 'Trebuchet MS', Tahoma, sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #080808;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: left;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">À échéance aujourd'hui</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="25%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 20px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #555555;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;">&nbsp;</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Total_estancia}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{Pagado}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 10px;padding-right: 20px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;text-align: right;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 14px;box-sizing: border-box;">{restante}</span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-3" width="50%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 5px;padding-top: 5px;vertical-align: top;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;"><span style="font-size: 16px;box-sizing: border-box;"><u style="box-sizing: border-box;"><strong style="box-sizing: border-box;">DÉTAILS</strong></u></span></p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📍 {address}</p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">📆 &nbsp;From {fechachekin} to {fechacheckout}</p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;padding-left: 40px;padding-right: 10px;padding-top: 10px;box-sizing: border-box;">
																<div style="font-family: sans-serif;box-sizing: border-box;">
																	<div class="" style="font-size: 12px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;mso-line-height-alt: 14.399999999999999px;color: #000000;line-height: 1.2;box-sizing: border-box;">
																		<p style="margin: 0;font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">👤 &nbsp;{numero_de_huespeds}</p>
																	</div>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #101112;direction: ltr;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;font-size: 9px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: center;mso-line-height-alt: 10.799999999999999px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;"><em style="box-sizing: border-box;">----<strong style="box-sizing: border-box;">{facturacion}</strong>----</em></p>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Headset Icon" title="Headset Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-right: 10px;box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Au moment de l'enregistrement, 
une provision bancaire de 150€ est effectuée en guise de garantie pour 
d'éventuels dommages à la propriété, perte de clés, retard au départ ou 
nettoyage final. Cette provision est libérée après l'inspection du 
logement à la fin de votre séjour.</p>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Les invités doivent respecter une
 période de silence de 23h00 à 8h00, maintenir les espaces communs 
propres et ordonnés, et traiter chacun avec respect et courtoisie. Le 
non-respect de ces règles peut entraîner des mesures correctives, y 
compris l'évacuation sans remboursement.</p>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 78.75px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="78.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
																	<p style="margin: 0;margin-bottom: 16px;box-sizing: border-box;line-height: inherit;">La présence de plus de personnes que convenu ou d'animaux domestiques non mentionnés dans la réservation entraînera une expulsion immédiate de la propriété.</p>
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">&nbsp;</p>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="width: 100%;padding-right: 0px;padding-left: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 70.875px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="70.875" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">Les invités doivent informer 
l'hôte dans les 48 heures suivant leur arrivée de tout dommage ou défaut
 constaté sur la propriété. Le défaut de notification peut entraîner que
 l'invité soit tenu responsable des dommages non déclarés.</p>
																</div>
															</td>
														</tr>
													</tbody></table>
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
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-left: 10px;width: 100%;padding-right: 0px;box-sizing: border-box;">
																<div class="alignment" align="center" style="line-height: 10px;box-sizing: border-box;">
																	<div style="max-width: 76.25px;box-sizing: border-box;"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display: block;height: auto;border: 0;width: 100%;box-sizing: border-box;" width="76.25" alt="Notes Icon" title="Notes Icon" height="auto"></div>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
												<td class="column column-2" width="75%" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;font-weight: 400;text-align: left;padding-bottom: 20px;padding-left: 10px;padding-right: 20px;padding-top: 20px;vertical-align: middle;border-top: 0px;border-right: 0px;border-bottom: 0px;border-left: 0px;box-sizing: border-box;">
													<table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="padding-bottom: 10px;box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 14px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: left;mso-line-height-alt: 16.8px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;"><strong style="box-sizing: border-box;">Apartamentos Cantabria ne sera pas responsable:</strong></p>
																</div>
															</td>
														</tr>
													</tbody></table>
													<table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt;mso-table-rspace: 0pt;word-break: break-word;box-sizing: border-box;">
														<tbody style="box-sizing: border-box;"><tr style="box-sizing: border-box;">
															<td class="pad" style="box-sizing: border-box;">
																<div style="color: #3d3d3d;direction: ltr;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;font-size: 12px;font-weight: 400;letter-spacing: 0px;line-height: 120%;text-align: justify;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;">
																	<p style="margin: 0;box-sizing: border-box;line-height: inherit;">I. La négligence ou les pannes de service imputables à des tiers.<br style="box-sizing: border-box;">II.
 Le dysfonctionnement des piscines, des zones de loisirs ou des 
installations sportives, dont l'utilisation relève de la responsabilité 
du client.<br style="box-sizing: border-box;">III. Les vols ou pertes subis par les clients sur la propriété.<br style="box-sizing: border-box;">IV. Les dommages personnels ou matériels causés par la force majeure ou des situations imprévues.<br style="box-sizing: border-box;">V. Les désagréments causés par le bruit des travaux à proximité.<br style="box-sizing: border-box;">VI. Les interruptions de la fourniture d'eau, de gaz ou d'électricité par les fournisseurs.<br style="box-sizing: border-box;">VII. Les retards dans la réparation des appareils et des chaudières par les services techniques officiels.</p>
																</div>
															</td>
														</tr>
													</tbody></table>
												</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
                    	<table class="row row-9" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; width: 750px; margin: 0 auto;" width="750">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; text-align: center;">
														<tr>
															<td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
																<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
																	<tr>
																		<td class="alignment" style="vertical-align: middle; text-align: center;"><!--[if vml]><table align="center" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																			<!--[if !vml]><!-->
																			<table class="icons-inner" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;" cellpadding="0" cellspacing="0" role="presentation"><!--<![endif]-->
																				<tr>
																					<td style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: undefined; color: #1e0e4b; vertical-align: middle; letter-spacing: undefined; text-align: center;"><a href="http://designedwithbeefree.com/" target="_blank" style="color: #1e0e4b; text-decoration: none;">+34 942679435</a></td>
																				</tr>
																			</table>
																		</td>
																	</tr>
																</table>
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


</body></html>"""
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
                                                                            <p style="font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">👤 &nbsp;{numero_de_huespeds}</p>
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
                        	<table class="row row-9" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; width: 750px; margin: 0 auto;" width="750">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; text-align: center;">
														<tr>
															<td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
																<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
																	<tr>
																		<td class="alignment" style="vertical-align: middle; text-align: center;"><!--[if vml]><table align="center" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																			<!--[if !vml]><!-->
																			<table class="icons-inner" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;" cellpadding="0" cellspacing="0" role="presentation"><!--<![endif]-->
																				<tr>
																					<td style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: undefined; color: #1e0e4b; vertical-align: middle; letter-spacing: undefined; text-align: center;"><a href="http://designedwithbeefree.com/" target="_blank" style="color: #1e0e4b; text-decoration: none;">+34 942679435</a></td>
																				</tr>
																			</table>
																		</td>
																	</tr>
																</table>
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
																		<p style="font-size: 12px;mso-line-height-alt: 14.399999999999999px;box-sizing: border-box;line-height: inherit;">👤 &nbsp;{numero_de_huespeds}</p>
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
                    	<table class="row row-9" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;">
						<tbody>
							<tr>
								<td>
									<table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; width: 750px; margin: 0 auto;" width="750">
										<tbody>
											<tr>
												<td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
													<table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; text-align: center;">
														<tr>
															<td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
																<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
																	<tr>
																		<td class="alignment" style="vertical-align: middle; text-align: center;"><!--[if vml]><table align="center" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
																			<!--[if !vml]><!-->
																			<table class="icons-inner" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;" cellpadding="0" cellspacing="0" role="presentation"><!--<![endif]-->
																				<tr>
																					<td style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: undefined; color: #1e0e4b; vertical-align: middle; letter-spacing: undefined; text-align: center;"><a href="http://designedwithbeefree.com/" target="_blank" style="color: #1e0e4b; text-decoration: none;">+34 942679435</a></td>
																				</tr>
																			</table>
																		</td>
																	</tr>
																</table>
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
    full_html_I = "<html><head><title>Documento Multi-página I</title></head><body>"
    full_html_S = "<html><head><title>Documento Multi-página S</title></head><body>"
    full_html_I += "</body></html>"
    full_html_S += "</body></html>"

# ⬇️ SOLO AQUÍ: métricas, detección y envío por separado
    raw_I_bytes = len(full_html_I.encode("utf-8"))
    raw_S_bytes = len(full_html_S.encode("utf-8"))
    logging.info("ISLA raw=%d KB, SOMO raw=%d KB", raw_I_bytes // 1024, raw_S_bytes // 1024)

    encoded_file_I = base64.b64encode(full_html_I.encode("utf-8")).decode("ascii")
    encoded_file_S = base64.b64encode(full_html_S.encode("utf-8")).decode("ascii")

    b64_I_bytes = len(encoded_file_I.encode("ascii"))
    b64_S_bytes = len(encoded_file_S.encode("ascii"))
    logging.info("ISLA b64=%d KB, SOMO b64=%d KB (Base64 ~+33%%)", b64_I_bytes // 1024, b64_S_bytes // 1024)

# Detector de contenido real (si quieres mantenerlo por seguridad)
    has_pages_I = "page-break-after" in full_html_I
    has_pages_S = "page-break-after" in full_html_S
    logging.info("has_pages -> ISLA=%s, SOMO=%s", has_pages_I, has_pages_S)

    # ... (resto: OAuth SendPulse, _send_single_attachment(...) y envíos condicionales)
    # Envío con SendPulse vía API SMTP (dos correos, uno por archivo)
    body_html_b64 = base64.b64encode(b"<strong>Los bienvenidos de hoy</strong>").decode("ascii")

    try:
        logging.info("enviarMail: solicitando token OAuth SendPulse")
        auth_resp = requests.post(
            "https://api.sendpulse.com/oauth/access_token",
            data={
                "grant_type": "client_credentials",
                "client_id": "75510a3b4821c413ad8ec42297856a41",
                "client_secret": "8110194a21fa751d2187c6b77b197a16",
            },
            timeout=20
        )
        logging.info("enviarMail: SendPulse OAuth status_code=%s", getattr(auth_resp, "status_code", "N/A"))
        auth_resp.raise_for_status()
        access_token = auth_resp.json().get("access_token")
        logging.info("enviarMail: token OAuth SendPulse obtenido (valor no logueado)")

        headers_sp = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Helper mínimo para enviar un email con un único adjunto
        def _send_single_attachment(filename: str, content_b64: str, label: str):
            payload = {
                "email": {
                    "html": body_html_b64,
                    "text": "Los bienvenidos de hoy",
                    "subject": f"📋🖨️ Chekins 🖨️📋 — {label}",
                    "from": {"name": "Apartamentos Cantabria",
                             "email": "reservas@apartamentoscantabria.net"},
                    "to": [
                        {"name": "Diego", "email": "diegoechaure@gmail.com"},
                        {"name": "Reservas", "email": "reservas@apartamentoscantabria.net"}
                    ],
                    "attachments_binary": {
                        filename: content_b64
                    }
                }
            }
            logging.info("enviarMail: enviando email '%s' (%s) a %s destinatarios",
                         filename, label, len(payload["email"]["to"]))
            resp_local = requests.post(
                "https://api.sendpulse.com/smtp/emails",
                json=payload,
                headers=headers_sp,
                timeout=30
            )
            logging.info("enviarMail: '%s' status_code=%s", filename, getattr(resp_local, "status_code", "N/A"))
            logging.info("enviarMail: '%s' respuesta=%s", filename, getattr(resp_local, "text", "")[:500])
            print(resp_local.status_code)
            print(resp_local.text)
            print(resp_local.headers)

        # Envía ISLA si tiene contenido real
        if has_pages_I:
            _send_single_attachment("ISLA.html", encoded_file_I, "ISLA")
        else:
            logging.info("enviarMail: ISLA sin páginas -> no se envía correo.")

        # Envía SOMO si tiene contenido real
        if has_pages_S:
            _send_single_attachment("SOMO.html", encoded_file_S, "SOMO")
        else:
            logging.info("enviarMail: SOMO sin páginas -> no se envía correo.")

    except Exception as e:
        logging.error("Error enviando email con SendPulse: %s", str(e))

def obtener_acceso_hostaway():
    logging.info("obtener_acceso_hostaway: solicitando token a %s", URL_HOSTAWAY_TOKEN)
    try:
        payload = {
            "grant_type": "client_credentials",
            "client_id": "81585",
            "client_secret": "0e3c059dceb6ec1e9ec6d5c6cf4030d9c9b6e5b83d3a70d177cf66838694db5f",
            "scope": "general"
        }
        headers = {'Content-type': "application/x-www-form-urlencoded", 'Cache-control': "no-cache"}
        response = requests.post(URL_HOSTAWAY_TOKEN, data=payload, headers=headers)
        logging.info("obtener_acceso_hostaway: status_code=%s", getattr(response, "status_code", "N/A"))
        # No cambiamos comportamiento (no raise_for_status aquí)
        token = response.json().get("access_token")
        logging.info("obtener_acceso_hostaway: token recibido correctamente (no se loguea el valor)")
        return token
    except requests.RequestException as e:
        logging.error(f"Error al obtener el token de acceso: {str(e)}")
        raise

def reservasHoy(arrivalStartDate, arrivalEndDate,token):
    url = f"https://api.hostaway.com/v1/reservations?arrivalStartDate={arrivalStartDate}&arrivalEndDate={arrivalEndDate}&includeResources=1&includePayments=1"
    logging.info("reservasHoy: GET %s", url)
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }
    try:
        response = requests.get(url, headers=headers)
        logging.info("reservasHoy: status_code=%s", getattr(response, "status_code", "N/A"))
        data = response.json()
        total = len(data.get("result", []))
        logging.info("reservasHoy: total reservas devueltas=%d", total)
    except Exception as e:
        logging.error("reservasHoy: error procesando respuesta: %s", str(e))
        raise SyntaxError(f"Error al procesar la reserva: {e}")
    return data

def direccionListing(token,listingId):
    url = f"https://api.hostaway.com/v1/listings/{listingId}?includeResources=1"
    logging.info("direccionListing: GET %s", url)
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers)
    logging.info("direccionListing: status_code=%s", getattr(response, "status_code", "N/A"))
    data = response.json()
    serie="A"
    try:
        for field in data['result']["customFieldValues"]:
            if field.get("customFieldId")==57829:
                mapped_value = value_mapping.get(field.get("value"), "A")  # Default a "A" si el valor no se encuentra en el mapeo
                serie = mapped_value
        addr = data['result'].get("address", "")
        logging.info("direccionListing: listingId=%s serie=%s len(address)=%s", listingId, serie, len(addr) if addr is not None else "None")
        return data['result']["address"],serie
    except Exception as e:
        logging.error("direccionListing: error parseando datos para listingId=%s -> %s", listingId, str(e))
        return data.get('result', {}).get("address", ""), "A"

def hayMascota(token,idReserva):
    url= f"https://api.hostaway.com/v1/financeField/{idReserva}"
    logging.info("hayMascota: GET %s", url)
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }
    try:
        response = requests.get(url, headers=headers)
        logging.info("hayMascota: status_code=%s", getattr(response, "status_code", "N/A"))
        res_json = response.json()
        data = res_json.get('result', [])
        found = any(element.get('name') == "petFee" for element in data)
        logging.info("hayMascota: idReserva=%s petFee=%s", idReserva, "SI" if found else "NO")
        return found
    except Exception as e:
        logging.error("hayMascota: error idReserva=%s -> %s", idReserva, str(e))
        return False


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