import flask
from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_mail import Message, Mail

from blog.forms.email import SendEmail


email_app = Blueprint('email_app', __name__, url_prefix='/', static_folder='../static')


def send_mail_to(data):
    """ Функция отправки эл. писем.
    """
    app = flask.current_app
    mail = Mail(app)
    with app.app_context():
        msg = Message("Ping!",
                      sender="admin.ping",
                      recipients=[data['email']])
        msg.body = data['message']
        mail.send(msg)


@email_app.route('/sendemail', endpoint='list', methods=['GET', 'POST'])
def send_email():
    form = SendEmail(request.form)
    if request.method == 'GET':
        print('GET')
        return render_template('email/list.html', form=form)

    elif request.method == 'POST':
        print('POST')
        data = {}
        data['email'] = request.form['email']
        data['message'] = request.form['message']
        send_mail_to(data)

        flash("Message sending")
        print('sending done')
        return render_template("email/list.html", form=form)



