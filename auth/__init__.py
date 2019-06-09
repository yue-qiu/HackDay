from flask import Blueprint, request, jsonify, session as ses, g, url_for
import hashlib
from Model import session, User
from conf import status
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

Auth = Blueprint('Auth', __name__)
active = {}


@Auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    email = request.form.get("email")
    qq = request.form.get("qq")
    wechat = request.form.get("wechat")
    if username and password and phone and email:
        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        user = session.query(User).filter(User.username == username).first()
        if not user:
            token = str(int(random.uniform(100, 10000)))
            active[token] = username
            user = User(username=username,
                        password=hash.hexdigest(),
                        avatar_url='http://pic1.cugapp.com/FikstAllXLweowBEXpy5FQxPd8td.jpg',
                        phone=phone,
                        email=email,
                        qq=qq,
                        wechat=wechat,
                        is_active=0)
            session.add(user)
            session.commit()
            send_mail(email, token)
            result = {
                "code": status.get("SUCCESS"),
                "MESSAGE": "邮件发送成功",
            }
            return jsonify(result)
        result = {
            "code": status.get("FAIL"),
            "message": "注册失败，用户名已存在",
        }
        return jsonify(result)
    result = {
        "code": status.get("FAIL"),
        "MESSAGE": "参数不足",
    }
    return jsonify(result)


@Auth.route("/authregister/<token>")
def authRefister(token):
    if active.get(token, None):
        user = session.query(User).filter(User.username == active.get(token)).first()
        user.is_active = 1
        session.commit()
        active.pop(token)
        return """<p>激活成功~<p>"""
    return """<P>Error<P>"""


@Auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        user = session.query(User).filter(User.username == username, User.password == hash.hexdigest()).first()
        if user and user.is_active:
            ses["uid"] = user.uid
            result = {
                "code": status.get("SUCCESS"),
                "MESSAGE": "登陆成功",
            }
            return jsonify(result)
        elif user and not user.is_active:
            session.delete(user)
            session.commit()
    result = {
        "code": status.get("FAIL"),
        "MESSAGE": "登陆失败，请检查用户密码",
    }
    return jsonify(result)


@Auth.route("/logout", methods=["GET"])
def logout():
    ses.pop("uid")
    result = {
        "code": status.get("SUCCESS"),
        "Message": "登出成功",
    }
    return jsonify(result)


def send_mail(to, token):
    sender = "1554525716@qq.com"
    password = "jshujpzyqaobifci"
    receivers = [to]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_msg = """
    <p>点击下面的链接，就可以完成账号认证啦~</p>
    <p><a href="{}">这是一个链接</a></p>
    """.format(url_for("Auth.authRefister", token=token, _external=True))

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("Fire", 'utf-8')
    message['To'] = Header("New User", 'utf-8')

    subject = '欢迎加入Fire'
    message['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, password)
    server.sendmail(sender, receivers, message.as_string())
    server.quit()


def verify_login():
    g.uid = ses.get("uid", None)
    if not g.uid:
        result = {
            "code": 300,
            "MESSAGE": "未登录",
        }
        return jsonify(result)
