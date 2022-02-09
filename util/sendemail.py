import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from config.read_ini import ReadIni


# 写信模板
msg = MIMEMultipart()
msg['Subject'] = "接口自动化测试报告"
msg['From'] = ReadIni("EMAIL", "sender")
msg['to'] = ReadIni("EMAIL", "receiver")

main_body = '<pre><h1>接口自动化测试报告，请查阅！`</h1></pre>'  # 正文的内容
# 通过os获取文件路径
annex = open("../reports.html", "r", encoding="utf-8").read()  # 附件，打开并且读取测试报告
# 添加正文到容器
body = MIMEText(main_body, "html", "utf-8")
msg.attach(body)

# 添加附件到容器
att = MIMEText(annex, "base64", "utf-8")
att["Content-Type"] = "application/octet-sream"
att["Content-Disposition"] = 'attachment;filename="opa_test_report.html"'  # 附件名称
msg.attach(att)


try:
    smtp = smtplib.SMTP_SSL(ReadIni("EMAIL", "smtpserver"), 465)
    # 登录
    smtp.login(ReadIni("EMAIL", "username"), ReadIni("EMAIL", "password"))
    # 发送邮件
    smtp.sendmail(ReadIni("EMAIL", "sender"), ReadIni("EMAIL", "receiver"), msg.as_string())
    print("发送邮件成功！！！")
    # 退出
    smtp.quit()

except smtplib.SMTPException:
    print("发送邮件失败！！！")
