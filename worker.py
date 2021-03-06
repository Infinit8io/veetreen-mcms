import pika
import tarfile
import json

pika_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
pika_channel = pika_connection.channel()

def callback(ch=None, method=None, properties=None, body=None):
    body_json = json.loads(body.decode(encoding='UTF-8'))
    alias = body_json["alias"]
    skel_tar = tarfile.open("skel.tar")

    for member_info in skel_tar.getmembers():
        skel_tar.extract(member_info, path="./veetreens/"+alias+"/")

    skel_tar.close()

    pika_channel.queue_declare(queue="refresh")
    pika_channel.basic_publish(
        exchange='',
        routing_key='refresh',
        body="pute",
        properties=pika.BasicProperties(delivery_mode=2)
    )

def work():
    pika_channel.queue_declare(queue="create_veetreen")
    pika_channel.basic_consume(callback, queue="create_veetreen", no_ack=True)
    pika_channel.start_consuming()

if __name__ == "__main__":
    work()
