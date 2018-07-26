from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_mail(app,msg):
    with app.app_context():
        mail.send(message=msg)


def send_mail(to,subject,tempalte,**kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + " " + subject,
        sender=app.config["MAIL_SENDER"], recipients=[to]
    )
    msg.body = render_template(tempalte+".txt", **kwargs)
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr