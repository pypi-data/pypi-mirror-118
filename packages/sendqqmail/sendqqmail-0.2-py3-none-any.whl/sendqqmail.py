import smtplib
from email.mime.text import MIMEText
def send(sender,receiver,psw,content,name,sub):
    msg = MIMEText(content)
    msg['From'] =name
    msg['Subject'] =sub
    msg['To'] = receiver
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(sender,psw)
        server.sendmail(sender,receiver,msg.as_string())
        server.quit()
        print("send already")
    except:
        print("fail")
    return
if __name__=='__main__':
    print(__name__)
    send()
