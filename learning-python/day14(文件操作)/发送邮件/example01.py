"""
example01 - 用Python发送邮件

SMTP 简单邮件传输协议

Author: lsy
Date: 2026/1/6
"""
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote
from email.utils import formataddr

# 邮件整体
email=MIMEMultipart()
# email['From']=Header('151...@163.com') # 发件人
# email['To']=Header('735..@qq.com,545...@qq.com') # 收件人
email['From'] = formataddr(('lsy', '151...@163.com'))
email['To'] ="735..@qq.com,545...@qq.com"

email['Cc']=Header('') # 抄送人
email['Subject']=Header('hello 你好','utf-8')
content='你好，Python'
email.attach(MIMEText(content,'plain','utf-8')) # plain纯文本
with open('../resources/demo.docx','rb') as f:
    attachment = MIMEText(f.read(), 'base64', 'utf-8')
    # 指定附件内容类型
    attachment['content-type']='application/octet-stream' # 二进制流
    # 如果文件有中文，使用 Header 处理中文文件名
    filename = Header('一个点.docx', 'utf-8').encode()
    # 指定如何处置内容
    attachment['Content-Disposition']=f'attachment; filename={filename}' # 附件的文件名
    email.attach(attachment) # 附件

# 创建 SMTP__SSL 对象，连接邮件服务器
smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
# 用户名和授权码进行登录
smtp_obj.login('151...@163.com', '授权码')
# 发送邮件（发件人，收件人，内容（字符串））
smtp_obj.sendmail('151...@163.com',['735...@qq.com','545...@qq.com'],email.as_string())

print('发送成功')