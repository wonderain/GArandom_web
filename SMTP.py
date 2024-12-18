import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback


def sendEmails(receivers,mail_msg):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = '1944149259@qq.com'  # 用户名
    mail_pass = "wljabemwxvsbbchc"  # 口令
    sender = '1944149259@qq.com'

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = '1944149259@qq.com'
    message['To'] = ';'.join(receivers)
    subject = 'GA对局通知'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        print('登录成功')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException :
        print(traceback.format_exc())
        print("Error: 无法发送邮件")





if __name__=='__main__':
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = '1944149259@qq.com'  # 用户名
    mail_pass = "wljabemwxvsbbchc"  # 口令
    sender = '1944149259@qq.com'
    receivers=['3249058247@qq.com']

    mail_msg = """Python 邮件发送测试"""
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = '1944149259@qq.com'
    message['To'] = ';'.join(receivers)
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        print('登录成功')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException :
        print(traceback.format_exc())
        print("Error: 无法发送邮件")