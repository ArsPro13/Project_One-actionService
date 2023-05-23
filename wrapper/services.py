from typing import IO
from .types import File
import smtplib

def mnk():
    return "Это результат"

from .types import Text 

def n100():
    return sum(range(100))

def f(a: File):
    return a.decode('utf8')

def ff(a: int, b: int):
    return a + b

def fff(a: int, b: int, c: int, d: int, e: int,):
    return a + b + c + d + e

def sendmail(email: str, text: str):
    mail_data={}
    mail = "bajbulatov.a.r@gymn1sam.ru"
    password = "20Amir04"
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    server.login(mail, password)
    server.sendmail(mail, email, text)
    server.quit()