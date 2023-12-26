import smtplib
from email.message import EmailMessage
from random import randint

def send_gmail(title:str, message:str, to_email:str) -> str:
    sender = 'toktorovkurmanbek92@gmail.com' #тут пишите свою почту
    password = 'xbubndyoakysjvuv'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = title 
    msg['From'] = sender 
    msg['To'] = to_email

    try:
        server.login(sender, password)
        server.send_message(msg)
        return "200 OK"
    except Exception as error:
        return f"Error: {error}"
    
# print(send_gmail('Geeks', 'Hello World and Geeks', 'ktoktorov144@gmail.com'))
    
def verify_user(email:str):
    sender = 'toktorovkurmanbek92@gmail.com' #тут пишите свою почту
    password = 'xbubndyoakysjvuv'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    random_number = randint(111111, 999999)

    msg = EmailMessage()
    msg.set_content(f"Ваш код верификации: {random_number}")

    msg['Subject'] = "Код верификации" 
    msg['From'] = sender 
    msg['To'] = email

    try:
        server.login(sender, password)
        server.send_message(msg)
        print("Код успешно отправлен в вашу почту")
    except Exception as error:
        print(f"Error: {error}")
    user_number = int(input("Введите код верификации с почты: "))
    if user_number == random_number:
        print("Успех")
    else:
        print("Неправильный код")
verify_user('toktorovkurmanbek92@gmail.com') #Внутри пишем свою почту
verify_user('ktoktorov2005@gmail.com') #Внутри пишем свою почту
verify_user('toktorovkurmanbek92@gmail.com') #Внутри пишем свою почту
verify_user('toktorovkurmanbek92@gmail.com') #Внутри пишем свою почту