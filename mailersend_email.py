import logging, os
from http import HTTPStatus

#Set API Key before importing mailersend libraries.
API_KEY = "your api key"
os.environ["MAILERSEND_API_KEY"]=API_KEY

from mailersend import emails

def sendSimpleEmail(lv_request):
    logging.debug(f'mailersend: Sending email')
    mailer = emails.NewEmail()
    print(mailer.mailersend_api_key)
    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": lv_request.get('fromName'),
        "email": lv_request.get('fromEmail'),
    }

    recipients = [
        {
            "name": lv_request.get('toName'),
            "email": lv_request.get('toEmail'),
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(lv_request.get('emailSubject'), mail_body)
    mailer.set_html_content(lv_request.get('emailHtmlBody'), mail_body)
    mailer.set_plaintext_content(lv_request.get('emailPlainTextBody'), mail_body)

    html_code = mailer.send(mail_body) #Return http status code 400 202 etc.
    html_code_phrase = str(int(html_code)).strip() + ": " + HTTPStatus(int(html_code)).phrase

    status = False #True-success | False-Failure
    if (int(html_code)%100)==2:
        status = True
    
    logging.debug(f'mailersend: {html_code_phrase}')

    lv_response = {'email_sent':status, 'html_code': html_code_phrase}
    return lv_response
    