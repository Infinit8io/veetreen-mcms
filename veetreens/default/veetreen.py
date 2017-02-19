from flask import Flask, render_template, request, redirect, url_for, session, make_response
from authomatic.providers import oauth2
from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from .models.Veetreen import Veetreen
from .conf import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY
REDIRECT_URI = "/login_callback"

import pika
import json


app = Flask(__name__)



app.secret_key = SECRET_KEY
pika_connection = None
channel = None
SERVER = "localhost"

AUTH_CONFIG = {
    'google': {
        'class_': oauth2.Google,
        'consumer_key': GOOGLE_CLIENT_ID,
        'consumer_secret': GOOGLE_CLIENT_SECRET,
        'scope': ['https://www.googleapis.com/auth/userinfo.profile',
                   'https://www.googleapis.com/auth/userinfo.email']
    }
}

authomatic = Authomatic(AUTH_CONFIG, SECRET_KEY, report_errors=False)


def load_pika():
    global channel
    global pika_connection
    pika_connection = pika.BlockingConnection(pika.ConnectionParameters(host=SERVER))
    channel = pika_connection.channel()
    channel.queue_declare(queue='create_veetreen')
    channel.queue_declare(queue='refresh')

load_pika()

@app.route('/')
def index():
    user_email = session.get('user_email', None)
    user_domain = session.get('user_domain', None)
    if user_email is None:
        return render_template('index.html')
    else:
        if user_domain is None:
            context = {
                'user_id': session.get('user_id', None),
                'user_name': session.get('user_name', None),
                'user_picture': session.get('user_pic', None)
            }
            return render_template('steps.html', context=context)
        else:
            context = {
                'user_id': session.get('user_id', None),
                'user_name': session.get('user_name', None),
                'user_picture': session.get('user_pic', None),
                'user_domain': user_domain
            }
            return render_template('theend.html', context=context)

@app.route('/login/<prov_name>/', methods=['GET', 'POST'])
def login(prov_name):
    response = make_response()
    result = authomatic.login(adapter=WerkzeugAdapter(request, response), provider_name=prov_name)
    if result:
        if result.user:
            result.user.update()
            session['user_id'] = result.user.id
            session['user_email'] = result.user.email
            session['user_name'] = result.user.name
            session['user_pic'] = result.user.picture
        return redirect(url_for('index'))
    return response

@app.route("/board")
def board():
    veetreens = Veetreen.get_all()
    return render_template('board.html', veetreens=veetreens)

@app.route("/create",methods=["POST"])
def create():
    global channel
    name = request.form["name"]
    alias = request.form["alias"]
    domain = request.form["domain"]
    user_side = request.form["user_side"] or None

    Veetreen(
        name=name,
        alias=alias,
        domain=domain
    ).create()

    channel.basic_publish(
        exchange='',
        routing_key='create_veetreen',
        body=json.dumps({
            "name": name,
            "alias": alias,
            "domain": domain
        }),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    if user_side is None:
        return redirect("/board")
    else:
        session['user_domain'] = domain
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
