from flask import Flask, render_template, request, redirect,g
from werkzeug.local import LocalProxy
from models.Veetreen  import Veetreen
import pika
import json

app = Flask(__name__)
SERVER = "localhost"


def get_channel():

    channel = getattr(g, '_channel', None)

    if not channel:
        pika_connection = pika.BlockingConnection(pika.ConnectionParameters(host=SERVER))
        channel = pika_connection.channel()
        channel.queue_declare(queue='create_veetreen')
        channel.queue_declare(queue='refresh')

    return channel

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

    Veetreen(
        name=name,
        alias=alias,
        domain=domain
    ).create()

    channel = LocalProxy(get_channel)

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

    channel.basic_publish(
        exchange='',
        routing_key='refresh',
        body="pute",
        properties=pika.BasicProperties(delivery_mode=2)
    )

    return redirect("/board")


if __name__ == "__main__":
    app.run()
