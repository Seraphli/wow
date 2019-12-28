import smtplib
from email.mime.text import MIMEText


def load_config():
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


cfg = load_config()
mail_host = cfg["mail_host"]
mail_user = cfg["mail_user"]
mail_pass = cfg["mail_pass"]
mail_postfix = cfg["mail_postfix"]
mailto_list = cfg["mail_list"]


def send_mail(to_list, sub, content):
    me = "SErAphLi" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    if send_mail(mailto_list, "Notification", "There is an event!"):
        print("Success")
    else:
        print("Failed")
