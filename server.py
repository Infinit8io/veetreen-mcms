from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from threading import Thread

from importlib import import_module

from pymongo import MongoClient

import pika
import worker

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        worker.work()

class WebServer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        httpd = make_server('', 8000, server_callback)
        print("Serving on port 8000...")
        httpd.serve_forever()

class MessageGetter(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        pika_channel.queue_declare(queue="refresh")
        pika_channel.basic_consume(dominique, queue="refresh", no_ack=True)
        pika_channel.start_consuming()

pika_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
pika_channel = pika_connection.channel()

db_collection = None
default = import_module("veetreens.default.veetreen")
veetreens = dict()
veetreens["default"] = default.app

def dominique(ch=None, method=None, properties=None, body=None):
    print("[INFO] Got refresh message !")
    for v in db_collection.find():
        act_veetreen = import_module("veetreens."+v["alias"]+".veetreen")
        if(v["domain"] not in veetreens.keys()):
            veetreens[v["domain"]] = act_veetreen.app
            print("[INFO] Veetreen at URL "+v["domain"]+" up !")


def server_callback(environ, start_response):
    for key,value in environ.items():
        if key == "HTTP_HOST":
            if value in veetreens.keys():
                return veetreens[value](environ, start_response)
            else:
                return veetreens["default"](environ, start_response)


if __name__ == "__main__":
    # Connexion à la DB
    db_client = MongoClient('localhost', 27017)
    db = db_client.veetreen
    db_collection = db.veetreens
    dominique()

    worker_thread = Worker()
    messagegetter_thread = MessageGetter()
    webserver_thread = WebServer()

    worker_thread.start()
    webserver_thread.start()
    messagegetter_thread.start()

    worker_thread.join()
    webserver_thread.join()
    messagegetter_thread.join()
