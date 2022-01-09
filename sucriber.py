import pika, sys, os, json
import pandas as pd
from hdfs import InsecureClient
import os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='theMusketeer')
    client_hdfs = InsecureClient('http://14.162.123.48:9870/', user='hadoop')

    dir = "/global"
    def callback(ch, method, properties, body):
        body = json.loads(body.decode())
        timestr = body["time"]
        data = body["data"]
        print(timestr)
        path = dir + '/data-' + timestr + '.json'
        # with open('./subcribe/data-' + timestr + '.json', 'w+', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        status = client_hdfs.status(path, strict=False)
        if not status:
            client_hdfs.write(path, data=json.dumps(data), encoding='utf-8')
        else:
            print("file " + path + " already exists!")

    channel.basic_consume(queue='theMusketeer', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)