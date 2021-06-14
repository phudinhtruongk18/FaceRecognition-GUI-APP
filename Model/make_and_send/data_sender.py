import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import telegram

import openpyxl as excel


def read_token_and_pass():
    sheet = excel.load_workbook(filename="Model/make_and_send/secret_infor.xlsx")
    data = sheet['Sheet1']
    temp_data = []
    for index, temp_value in enumerate(data.values):
        if index == 0:
            continue
        if temp_value[0] is None:
            break
        temp_data.append(temp_value)
    return temp_data[0]


def send_result_to_telegram(receiver_id, filename, my_telegram_token):
    # Tạo make_and_send
    bot = telegram.Bot(token=my_telegram_token)
    bot.sendDocument(chat_id=receiver_id, document=open(filename, 'rb'),
                     caption="Notification From Attendance Recorder System")


def send_gmail(fromaddr, password, toaddr, filepath, filename):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Notification From Attendance Recorder System"
    body = "Excel file"
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filepath, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    filename += ".xlsx"
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def send_to_gmail_and_telegram(filename):
    # get array data from text file
    my_secret_data = read_token_and_pass()

    filepath = "View/Summary/" + filename + ".xlsx"
    try:
        # first is token key
        my_telegram_token = my_secret_data[0]
        receiver_id = my_secret_data[1]
        # send result to telegram user
        send_result_to_telegram(receiver_id, filepath, my_telegram_token)
        print("Send To Telegram Successfully")
    except Exception as e:
        print("Fail to send telegram")
        print(e)

    try:
        username = my_secret_data[2]
        password = my_secret_data[3]
        send_gmail(fromaddr=username, password=password, toaddr=username, filepath=filepath, filename=filename)
        print("Send To Gmail Successfully")
    except Exception as e:
        print("Fail to send Gmail")
        print(e)
