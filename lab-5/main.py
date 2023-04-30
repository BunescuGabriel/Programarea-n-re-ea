import email
import imaplib
import poplib
import smtplib
import ssl
import os
from email import encoders
from email import header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from tkinter import filedialog
import tkinter as tk


username = 'gabriel.labpr@outlook.com'
password = 'qwerty12345'

smtp_port = 587
smtp_host = 'smtp.office365.com'

host = 'outlook.office365.com'
path = 'C:/Users/gabyb/Desktop/PR/lab-5/downloads/'
attach_path = 'C:/Users/gabyb/Desktop/PR/lab-5/attachments/'


def send_mail():
    message = MIMEMultipart()
    message['From'] = 'gabriel.labpr@outlook.com'
    print("adresa unde doriti sa trimiteti emailul:")
    send_list = []
    while True:
        addr = input()
        if addr == '/next':
            break
        else:
            send_list.append(addr)
    message['To'] = ', '.join(send_list)
    # message['To'] = input()
    message['Subject'] = input('Subiectul:')
    body = input('Textul emailului:')
    attach_flag = input("Doriti sa atasati un fisier?\nDa: 1\nNu: 2\n")
    if attach_flag == '1':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        attachment = open(file_path, 'rb')
        attachment_pack = MIMEBase('application', 'octet-stream')
        attachment_pack.set_payload((attachment).read())
        encoders.encode_base64(attachment_pack)
        attachment_pack.add_header(
            'Content-Disposition', 'attachment; filename= '+file_path.split('/')[-1])
        message.attach(attachment_pack)
    else:
        pass

    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()

    try:
        tie = smtplib.SMTP(smtp_host, smtp_port)
        tie.starttls()
        tie.login(username, password)
        print("conected to smtp server\n")

        print(f"Sending email to - {message['From']}")
        tie.sendmail(username, send_list, text)
        print("email succesfully sent")

    except:
        print("ERROR")


def get_imap():
    imap = imaplib.IMAP4_SSL(host)
    imap.login(username, password)
    imap.select('Inbox')
    typ, data = imap.search(None, 'ALL')
    sbject = ''
    sender = ''
    msg_count = 1
    for num in data[0].split():
        typ, msg_data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if bool(fileName):
                filePath = os.path.join(attach_path, fileName)
                if not os.path.exists('C:/Users/gabyb/Desktop/PR/lab-5/attachments/'):
                    os.makedirs('C:/Users/gabyb/Desktop/PR/lab-5/attachments/')
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                subject = str(msg).split("Subject: ", 1)[
                    1].split("\nTo:", 1)[0]

        print(f'Email: {msg_count}: {msg["Subject"]}')
        msg_count += 1  # incrementa numărul de mesaje după fiecare mesaj

    print("Doriti sa deaschideti un anumit email?")
    flag = input("Da: 1\nNu:2\n")
    if flag == '1':
        selected = input("Introduceti indexul mesajului dorit:")
        selected = int(selected)
        message_id = data[0].split()[selected - 1]  # scădeți 1 pentru a obține indexul bazat pe 0
        status, msg_data = imap.fetch(message_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        sbject = msg.get('Subject')
        sender = msg.get('From')
        body = ''
        filename = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_payload(decode=True).decode('utf-8')
                if part.get_content_type() == 'su':
                    body += part.get_payload(decode=True).decode('utf-8')
                if part.get_content_type() == 'application/octet-stream':
                    filename = part.get_filename()

        else:
            # Dacă mesajul nu are mai multe părți, obțineți încărcătura utilă
            body += msg.get_payload(decode=True).decode('utf-8')

        print(
            f'#######################   Texutl emailului: #########################\n{body}')
        print(
            f'#######################   atasamente:##############################\n{filename}')
    elif flag == '2':
        pass
    if flag == '1':
        print("Doriti sa raspundeti la acest email?\n")
        flag_res = input("Da: 1\nNu:2\n")
        if flag_res == '1':

           # Conectați-vă la serverul SMTP și trimiteți mesajul de răspuns
            reply_msg = MIMEMultipart()
            reply_subject = f"Re: {sbject}"
            reply_body = input("Tastati raspunsul:\n")
            reply_body = MIMEText(reply_body)
            reply_msg['To'] = sender
            reply_msg['From'] = username
            reply_msg['Subject'] = reply_subject
            reply_msg.attach(reply_body)
            attach_flag = input("Doriti sa atasati un fisier?\nDa: 1\nNu: 2\n")
            if attach_flag == '1':
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                attachment = open(file_path, 'rb')
                attachment_pack = MIMEBase('application', 'octet-stream')
                attachment_pack.set_payload((attachment).read())
                encoders.encode_base64(attachment_pack)
                attachment_pack.add_header(
                    'Content-Disposition', 'attachment; filename= ' + file_path.split('/')[-1])
                reply_msg.attach(attachment_pack)
            else:
                pass

            text = reply_msg.as_string()

            try:
                tie = smtplib.SMTP(smtp_host, smtp_port)
                tie.starttls()
                tie.login(username, password)
                print("conected to smtp server\n")

                tie.sendmail(username, sender, text)
                print("email succesfully sent")
                tie.quit()
            except:
                print("ERROR")
        else:
            pass


def get_pop3():
    pop = poplib.POP3_SSL(host, 995)
    pop.user(username)
    pop.pass_(password)

    if not os.path.exists(path):
        os.makedirs(path)

    nr_message = len(pop.list()[1])
    print(f"There are {nr_message} messages in the mailbox:")
    for i in range(1, nr_message+1):
        response = pop.top(i, 0)
        header = email.message_from_bytes(b'\r\n'.join(response[1]))
        print(f"Message {i}: {header['Subject']}")

    message_number = int(input("Introduceți numărul mesajului pe care doriți să îl vizualizați: "))

    # Obțineți mesajul selectat și il analizam
    response = pop.retr(message_number)
    raw_message = response[1]
    message = b'\r\n'.join(raw_message).decode('utf-8')
    parsed_message = email.message_from_string(message)

    # Verificați atașamentele și afișați numele fișierului dacă este găsit
    filename = None
    for part in parsed_message.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()

    # Obțineți corpul mesajului
    body = None
    for part in parsed_message.walk():
        if part.get_content_type() == 'text/plain':
            body = part.get_payload(decode=True).decode('utf-8')
            break

    print(f"#######################   Textul emailului: #########################\n{body}")
    if filename:
        print(f"#######################   atasament:  ################################\n{filename}")

    response = input("Doriți să vedeți atașamentul? (y/n): ")
    if response.lower() == 'y' and filename:
        with open(filename, 'wb') as f:
            attachment_data = None
            for part in parsed_message.walk():
                if part.get_content_disposition() == 'attachment':
                    attachment_data = part.get_payload(decode=True)
                    break
            if attachment_data:
                f.write(attachment_data)
                print(f"Atașamentul a fost salvat în {filename}")
        with open(filename, 'r') as f:
            print(f"Conținutul atașamentului {filename} este:\n{f.read()}")
    else:
        print("Niciun atașament de vizualizat sau utilizatorul a optat pentru a nu-l vedea.")
        
    response = input("Doriți să răspundeți la acest mesaj? (y/n): ")
    if response.lower() == 'y':
        response = input("Introduceți mesajul de răspuns: ")
    if response:
        reply_message = MIMEMultipart()
        reply_message['From'] = parsed_message['To']
        reply_message['To'] = parsed_message['From']
        reply_message['Subject'] = "Re: " + parsed_message['Subject']
        reply_message.attach(MIMEText(response))
        
        attach_flag = input("Doriti sa atasati un fisier?\nDa: 1\nNu: 2\n")
        if attach_flag == '1':
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            attachment = open(file_path, 'rb')
            attachment_pack = MIMEBase('application', 'octet-stream')
            attachment_pack.set_payload((attachment).read())
            encoders.encode_base64(attachment_pack)
            attachment_pack.add_header(
                'Content-Disposition', 'attachment; filename= ' + file_path.split('/')[-1])
            reply_message.attach(attachment_pack)


        smtp_server = smtplib.SMTP(smtp_host, smtp_port)
        smtp_server.starttls()
        smtp_server.login(username, password)
        smtp_server.sendmail(parsed_message['To'], parsed_message['From'], reply_message.as_string())
        
        
        print("Mesajul de răspuns a fost trimis cu succes.")
    else:
        print("Nu a fost introdus niciun mesaj de răspuns. Mesajul nu va fi trimis.")
    
def run():
    print('##########################################################################\n'
          '################             LABORATOR 5          ########################\n'
          '################                                  ########################\n'
          '##########################################################################\n')
    print('Ce doriti sa efectuati?\n')
    
    while True:
        print('\n''Verificare inbox-ului prin IMAP:  1\n'
          'Verificarea inbox-ului prin POP3:  2\n'
          'Trimiterea unui email: 3\n')
        
        print('Ce doriti sa efectuati?\n')
        case = int(input())
        if case == 1:
            get_imap()
        elif case == 2:
            get_pop3()
        elif case == 3:
            send_mail()


if __name__ == '__main__':
    run()
