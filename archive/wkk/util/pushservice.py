#-*-coding:utf-8-*-

#import getpass #如果需要交互获取密码
#pwd_input = getpass.getpass('Password:')
import time
import smtplib
import email.utils
from email.mime.text import MIMEText
#Initialize mail information
mailto_list = ['wdxtub@qq.com']
mail_host = 'smtp.sina.com'
mail_postfix = 'sina.com'   #发件箱后缀
mail_user = 'pushwkk'
mail_pass = 'wangtt33'

mail_host = 'smtp.163.com'
mail_postfix = '163.com'   #发件箱后缀
mail_user = 'wdxtub'
mail_pass = ''
mail_from = '@'.join([mail_user,mail_postfix]) #收件箱


def push():
    content = "Hello wkkpush"
    msg = MIMEText(content,_subtype='plain',_charset='utf8')
    msg['From'] = email.utils.formataddr(('Author',mail_from)) #str type
    msg['To'] = email.utils.formataddr(('Recipient',mailto_list)) #mail to list
    msg['Subject'] = 'Test from python!'
    msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')#定义发送时间

    try:
        server = smtplib.SMTP(mail_host, 25)
        server.login(mail_user,mail_pass)
        server.sendmail(mail_from,mailto_list,msg.as_string()) #mail to list recipient
    except Exception,e: #try中有异常则执行
        print 'Mail passed unsuccessfully!\n',str(e)
    else: #try中没有异常则执行
        print 'Mail passed successfully!'
    finally: #try中有无异常都执行
        server.close()

if __name__ == '__main__':
    push()

