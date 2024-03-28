
import logging
import os
import base64
from io import BytesIO
import requests
from datetime import datetime
from weasyprint import HTML
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import azure.functions as func

URL_HOSTAWAY_TOKEN = "https://api.hostaway.com/v1/accessTokens"
app = func.FunctionApp()
def enviarMail(reservas,token):
    base_html = """ <!DOCTYPE html><html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en" style="box-sizing:border-box"><head style="box-sizing:border-box"><title style="box-sizing:border-box"></title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" style="box-sizing:border-box"><meta name="viewport" content="width=device-width,initial-scale=1" style="box-sizing:border-box"><!--[if mso]><xml><o:officedocumentsettings><o:pixelsperinch>96</o:pixelsperinch><o:allowpng></o:officedocumentsettings></xml><![endif]--><!--[if !mso]><!--><!--<![endif]--></head><body style="background-color:#fff;margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none;box-sizing:border-box"><table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:10px;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:10px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:15px;padding-right:15px;width:100%;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:225px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/public/users/Integrators/BeeProAgency/1147963_1133632/Logo%20AC%202024%281%29.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="225" height="auto"></div></div></td></tr></table><table class="heading_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:5px;padding-left:15px;padding-right:15px;padding-top:5px;text-align:center;width:100%;box-sizing:border-box"><h1 style="margin:0;color:#393939;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:32px;font-weight:700;letter-spacing:-1px;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:38.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Apartamento}<br style="box-sizing:border-box"></span></h1></td></tr></table><table class="divider_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;padding-right:10px;box-sizing:border-box"><div class="alignment" align="center" style="box-sizing:border-box"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="65%" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="divider_inner" style="font-size:1px;line-height:1px;border-top:2px solid #3d3d3d;box-sizing:border-box"><span style="box-sizing:border-box">&#8202;</span></td></tr></table></div></td></tr></table><table class="heading_block block-4" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><h3 style="margin:0;color:#3e3e3e;direction:ltr;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;font-size:22px;font-weight:400;letter-spacing:normal;line-height:120%;text-align:center;margin-top:0;margin-bottom:0;mso-line-height-alt:26.4px;box-sizing:border-box"><span class="tinyMce-placeholder" style="box-sizing:border-box">{Nombre}</span></h3></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#d4d4d4;border-bottom:17px solid transparent;border-left:17px solid transparent;border-radius:30px;border-right:17px solid transparent;border-top:17px solid transparent;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><u style="box-sizing:border-box"><span style="font-size:16px;box-sizing:border-box"><strong style="box-sizing:border-box">PAGOS</strong></span></u></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">Total Estancia:</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">Realizado:</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:50px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:'Trebuchet MS',Tahoma,sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#080808;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:left;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">A pagar:</span></p></div></div></td></tr></table></td><td class="column column-2" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#555;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box">&nbsp;</span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Total_estancia}</span></p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{Pagado}</span></p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:10px;padding-right:20px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;text-align:right;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:14px;box-sizing:border-box">{restante}</span></p></div></div></td></tr></table></td><td class="column column-3" width="50%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="text_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit"><span style="font-size:16px;box-sizing:border-box"><u style="box-sizing:border-box"><strong style="box-sizing:border-box">DETALLES</strong></u></span></p></div></div></td></tr></table><table class="text_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📍 {address}</p></div></div></td></tr></table><table class="text_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">📆 &nbsp;Del {fechachekin} al {fechacheckout</p></div></div></td></tr></table><table class="text_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;padding-left:40px;padding-right:10px;padding-top:10px;box-sizing:border-box"><div style="font-family:sans-serif;box-sizing:border-box"><div class style="font-size:12px;font-family:Montserrat,'Trebuchet MS','Lucida Grande','Lucida Sans Unicode','Lucida Sans',Tahoma,sans-serif;mso-line-height-alt:14.399999999999999px;color:#000;line-height:1.2;box-sizing:border-box"><p style="margin:0;font-size:12px;mso-line-height-alt:14.399999999999999px;box-sizing:border-box;line-height:inherit">👤 &nbsp;{Numero de huespeds}</p></div></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;background-color:#fff;color:#000;border-radius:2px;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:20px;padding-right:10px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:75.375px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/9rf/x64/d4m/verificado.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="75.375" alt="Headset Icon" title="Headset Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-right:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Al momento de completar el check-in se realizará una<strong style="box-sizing:border-box">retención bancaria&nbsp;de 150€</strong>como garantía de posibles deterioros de la vivienda, perdida de llaves, retraso en la salida ó limpieza final. Esta retención se liberará tras la revisión del alojamiento posterior al check-out.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:83.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/l0w/k40/183/ruido.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="83.75" alt="Paper Sheet With a Chart Icon" title="Paper Sheet With a Chart Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben<strong style="box-sizing:border-box">respetar un horario de silencio</strong>de 23:00 a 08:00 horas, mantener las áreas comunes limpias y ordenadas, y tratar a todos con respeto y cortesía. El incumplimiento de estas normas puede resultar en medidas correctivas, incluido el desalojo sin reembolso.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-5" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-left:20px;padding-right:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:83.75px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/r2q/b8w/l96/business-people.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="83.75" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">&nbsp;</p><p style="margin:0;margin-bottom:16px;box-sizing:border-box;line-height:inherit">La estancia de<strong style="box-sizing:border-box">más personas de las acordadas</strong>, o de animales de compañía no especificados en la reserva, conllevará la expulsión inmediata de la propiedad.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">&nbsp;</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-6" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:30px;padding-left:20px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="width:100%;padding-right:0;padding-left:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:75.375px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/75f/whx/f0u/broken-pottery-svgrepo-com.svg" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="75.375" alt="Piggy Bank Icon" title="Piggy Bank Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit">Los huéspedes deben informar al anfitrión de<strong style="box-sizing:border-box">cualquier daño</strong>o<strong style="box-sizing:border-box">desperfecto</strong>en la propiedad dentro de las 48 horas siguientes a su llegada. La omisión de este reporte puede conllevar a que el huésped sea considerado responsable de los daños no declarados.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-7" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="25%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-left:10px;width:100%;padding-right:0;box-sizing:border-box"><div class="alignment" align="center" style="line-height:10px;box-sizing:border-box"><div style="max-width:81.25px;box-sizing:border-box"><img src="https://d487b3526b.imgdist.com/pub/bfra/tk3qo566/qkr/hzx/unq/aceptar.png" style="display:block;height:auto;border:0;width:100%;box-sizing:border-box" width="81.25" alt="Notes Icon" title="Notes Icon" height="auto"></div></div></td></tr></table></td><td class="column column-2" width="75%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:20px;padding-left:10px;padding-right:20px;padding-top:20px;vertical-align:middle;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><table class="paragraph_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="padding-bottom:10px;box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;font-weight:400;letter-spacing:0;line-height:120%;text-align:left;mso-line-height-alt:16.8px;box-sizing:border-box"><p style="margin:0;box-sizing:border-box;line-height:inherit"><strong style="box-sizing:border-box">Apartamentos Cantabria no se hará responsable por:</strong></p></div></td></tr></table><table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;word-break:break-word;box-sizing:border-box"><tr style="box-sizing:border-box"><td class="pad" style="box-sizing:border-box"><div style="color:#3d3d3d;direction:ltr;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;font-weight:400;letter-spacing:0;line-height:120%;text-align:justify;mso-line-height-alt:14.399999999999999px;box-sizing:border-box"><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">I. Negligencias o fallos de servicios atribuibles a terceros.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">II. Mal funcionamiento de piscinas, áreas recreativas o instalaciones deportivas, cuyo uso será bajo la responsabilidad del huésped.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">III. Robos o pérdidas sufridas por los huéspedes en la propiedad.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">IV. Daños personales o materiales ocasionados por fuerzas mayores o situaciones imprevistas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">V. Molestias por ruidos de obras cercanas.</p><p style="margin:0;margin-bottom:1px;box-sizing:border-box;line-height:inherit">VI. Cortes en el suministro de agua, gas o electricidad por parte de proveedores.</p><p style="margin:0;box-sizing:border-box;line-height:inherit">VII. Retrasos en las reparaciones de electrodomésticos y calderas por servicios técnicos oficiales.</p></div></td></tr></table></td></tr></tbody></table></td></tr></tbody></table><table class="row row-8" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0 0 30px 30px;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:10px;padding-left:20px;padding-right:20px;padding-top:10px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><div class="spacer_block block-1" style="height:10px;line-height:10px;font-size:1px;box-sizing:border-box">&#8202;</div></td></tr></tbody></table></td></tr></tbody></table><table class="row row-9" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;box-sizing:border-box"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td style="box-sizing:border-box"><table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0;mso-table-rspace:0;border-radius:0;color:#000;width:790px;margin:0 auto;box-sizing:border-box" width="790"><tbody style="box-sizing:border-box"><tr style="box-sizing:border-box"><td class="column column-1" width="100%" style="mso-table-lspace:0;mso-table-rspace:0;font-weight:400;text-align:left;padding-bottom:5px;padding-top:5px;vertical-align:top;border-top:0;border-right:0;border-bottom:0;border-left:0;box-sizing:border-box"><div class="spacer_block block-1" style="height:20px;line-height:20px;font-size:1px;box-sizing:border-box">&#8202;</div></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></body></html>"""

    # Generar el HTML completo con 3 páginas
    full_html = "<html><head><title>Documento Multi-página</title></head><body>"
    try:
        for reserva in reservas:
            listingID=reserva["listingMapId"]
            direccionListing(token,listingID)
            full_html += base_html.format(
                Apartamento=reserva["listingName"],
                Nombre=reserva["guestName"],
                Total_estancia=str(reserva["totalPrice"]) + " " + reserva["currency"],
                Pagado="no se",
                restante=reservas["remainingBalance"],
                address="Ejemplo dirección",
                fechachekin=reserva["arrivalDate"],
                fechacheckout=reserva["departureDate"],
                Numero_de_huespeds=str(reserva["numberOfGuests"])
        ) + "<div style='page-break-after: always;'></div>"
    except Exception as e:
        raise KeyError(f"La reserva no contiene 'listingMapId': {reservas}")
        
    full_html += "</body></html>"
    # Generar el PDF desde HTML y mantenerlo en memoria
    pdf_bytes_io = BytesIO()
    HTML(string=full_html).write_pdf(target=pdf_bytes_io)
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
    
    url = f"https://api.hostaway.com/v1/reservations?arrivalStartDate={arrivalStartDate}&arrivalEndDate={arrivalEndDate}&includeResources=1" 

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
    url = f"https://api.hostaway.com/v1/listings/{listingId}" 

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-type': "application/json",
        'Cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data["address"]


@app.schedule(schedule="0 0 10 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def crecionBienvenido(myTimer: func.TimerRequest) -> None:
    token = obtener_acceso_hostaway()
    hoy = datetime.now().strftime('%Y-%m-%d')
    reservas= reservasHoy(hoy,hoy,token)
    enviarMail(reservas,token)
    logging.info('Python timer trigger function executed.')