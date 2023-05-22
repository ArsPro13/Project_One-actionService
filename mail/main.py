import smtplib
import mail_data

server = smtplib.SMTP_SSL('smtp.gmail.com:465')
server.login(mail_data.mail, mail_data.password)
server.sendmail(mail_data.mail, "Write the email you want to send the message to", "Write your message")
server.quit()
