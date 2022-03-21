import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def main(email, chapter):
    
    sender = 'onepiece.manga.bot@gmail.com'
    password = 'Trafalgarlaw'
    body = 'Viel spaß beim lesen'


    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

    cwd = os.getcwd()
    folder = "One_Piece_Manga"
    cwd = os.path.join(cwd, folder)

    if not os.path.exists(cwd):
        print("Folder does not exist")
    else:
        os.chdir(cwd)


    pdf = str(chapter) + '.pdf'

   
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = email
    message['Subject'] = 'Chapter ' + pdf.split('.')[0]

    message.attach(MIMEText(body, 'plain'))

    # open the file in binary
    binary_pdf = open(pdf, 'rb')
    payload = MIMEBase('application', 'octate-stream', Name=pdf)
    payload.set_payload((binary_pdf).read())

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition',
                        'attachment', filename=pdf)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, email, text)
    session.quit()

