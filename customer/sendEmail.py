# -*- coding: UTF-8 -*-
# @author youerning
# @email 673125641@qq.com

import sys
import base64
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from io import BytesIO
from os import path
import csv
import time
from jinja2 import Template
from selenium.webdriver import Chrome



if __name__ == "__main__":

    jenkins_url = r'http://125.94.117.177:20410/login'
    jenkins_username = 'admin'
    jenkins_passwd = 111111

    # 发送邮件所需的信息
    mail_to = ["1033474912@qq.com", "feiniao.gjh@bitsun-inc.com"]
    smtp_host = "smtp.126.com"
    smtp_username = "springfall3015@126.com"
    smtp_password = "TIKDVKBNQOWWPMKM"
    subject = "自动化测试用例测试结果"
    from_ = "自动化测试用例执行结果"

    image_path = 'D:/jenkins_workspace/workspace/pc_management/allure-report/allure.png'
    file = 'D:/jenkins_workspace/workspace/pc_management/allure-report/data/behaviors.csv'

    # 用于发个收件人的逗号
    COMMASPACE = ","

    EMAIL_TEMPLATE = """<html>
    <head>
        <style type="text/css">
            table
            {
                border-collapse: collapse;
                margin: 0 auto;
                text-align: center;
            }

            table td, table th
            {
                border: 1px solid #cad9ea;
                color: #666;
                height: 30px;
            }

            table thead th
            {
                background-color: #CCE8EB;
                width: 100px;
            }

            table tr:nth-child(odd)
            {
                background: #fff;
            }

            table tr:nth-child(even)
            {
                background: #F5FAFA;
            }
        </style> 
    </head>
    <body>
    <p>一共有以下{{record_size}}条数据</p>
    <table width="90%" class="table">
        <thead>
            <tr>
            {% for label in labels %}
                <th>{{label}}</th>
            {% endfor %}
            </tr>
        </thead>
        <tbody>
    {% for item in items %}
        <tr>
        {% for value in item %}
            <td>{{value}}</td>
        {% endfor %}
        </tr>
    {% endfor %}
        </tbody>
    </table>
    </html>"""

    EMAIL_IMAGE_TEMPLATE = """<html>
    <head>
    <title>Page Title</title>
    </head>
    <body>
    <h3>----------------------测试结果-----------------------</h3>
    <p>测试用例总数:{{total_num}}， 失败用例数:{{failed_num}}，pass用例数:{{passed_num}}，broken用例数:{{broken_num}}，skipped用例数:{{skipped_num}} </p>
    <h3>测试结果综述图：</h3>
    <p><img src="cid:{{image_name}}" height="112" width="200" ></p>
    </body>
    </html>
    """

    EMAIL_ONLINE_IMAGE_TEMPLATE = """<html>
    <head>
    <title>Page Title</title>
    </head>
    <body>
    <h3>这是一张图片</h3>
    <p><img src="cid:{{image_name}}" ></p>
    </body>
    </html>
    """


    def listToDict(datas):
        result = {}
        data = {}
        if not isinstance(datas, list):
            raise TypeError("参数需要是list类型，该类型不对{}".format(type(datas)))

        for i in range(0, min(len(datas[0]), len(datas[1]))):
            result.update({datas[0][i]: datas[1][i]})
        total = 0
        for i in datas[1]:
            if i:
                total = total + int(i)
        data.update(
            {"total_num": total, "failed_num": result.get('FAILED', '0'), "passed_num": result.get('PASSED', "0"),
             "broken_num": result.get('BROKEN', "0"), "skipped_num": result.get('SKIPPED', "0")})
        return data


    def create_image_eamil_contant(fp):

        tpl = Template(EMAIL_IMAGE_TEMPLATE)
        if not path.exists(fp):
            sys.exit("要发送的本地图片不存在")

        results = {}
        with open(file, 'r') as f:
            file_datas = csv.reader(f)
            temps = []
            for data in file_datas:
                temps.append(data)
            results = listToDict(temps)

        msg = MIMEMultipart("related")
        image_name = "demo"

        with open(fp, "rb") as rf:
            mime_image = MIMEImage(rf.read())
            # 注意: 一定需要<>括号
            mime_image.add_header("Content-ID", "<%s>" % image_name)
            msg.attach(mime_image)

        # 渲染邮件文本内容
        text = tpl.render(image_name=image_name, total_num=results.get("total_num", "0"),
                          failed_num=results.get("failed_num", "0"), passed_num=results.get("passed_num", "0"),
                          broken_num=results.get('broken_num', '0'), skipped_num=results.get('skipped_num', '0'))
        msg_alternative = MIMEMultipart("alternative")
        msg_alternative.attach(MIMEText(text, "html", "utf-8"))

        msg.attach(msg_alternative)

        return msg


    def send_email(msg, mail_to, smtp_host, smtp_username, smtp_password, subject, from_):
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = Header(from_, "utf-8")
        if not isinstance(mail_to, list):
            mail_to = [mail_to]
        msg["To"] = COMMASPACE.join(mail_to)

        try:
            client = smtplib.SMTP(smtp_host)
            client.login(smtp_username, smtp_password)
            client.sendmail(smtp_username, mail_to, msg.as_string())
            return True
        except Exception:
            print("发送邮件失败")
        finally:
            client.quit()


    def send_local_image_email():
        msg = create_image_eamil_contant(image_path)
        send_email(msg, mail_to, smtp_host, smtp_username, smtp_password, subject, from_)


    try:
        driver = Chrome()
        driver.get(jenkins_url)
        driver.maximize_window()
        time.sleep(10)
        driver.find_element_by_id('j_username').send_keys(jenkins_username)
        driver.find_element_by_name('j_password').send_keys(jenkins_passwd)
        driver.find_element_by_name('Submit').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="job_pc_management"]/td[3]/a').click()
        time.sleep(5)
        if driver.find_elements_by_xpath('//*[@id="main-panel"]/h1[contains(text(), "工程")]'):
            driver.find_element_by_link_text('Allure Report').click()
            time.sleep(10)
        if driver.find_elements_by_xpath('//*[@id="content"]//span[contains(text(), "Allure")]'):
            if not driver.get_screenshot_as_file(image_path):
                raise Exception("截图出现错误")
        driver.quit()

        send_local_image_email()
    except:
        raise Exception("运行出现错误")