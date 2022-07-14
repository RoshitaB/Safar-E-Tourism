from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from django.template.loader import get_template
import smtplib
def sendMail(email,payment_id,cold_coffee,context_dict):
    template = get_template('monumentTicket.html')
    html  = template.render(context_dict)
    email_user = 'safar.etourism@yahoo.com'
    email_password = 'xlbnrczhgcufnprh'
    email_send = email
    subject = f'Your ticket for {cold_coffee.monument} is confirmed.'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    
    # part2 = MIMEText(html, "html")
    # msg.attach(part2)
    # comment: configure your own file path
    # filename = "Frontend/build/static/Generated_QR/test.png"
    # attachment  =open(filename,'rb')

    filename = "Frontend/build/static/Generated_ticket/"+payment_id+".pdf"
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.mail.yahoo.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()