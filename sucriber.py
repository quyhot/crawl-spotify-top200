import pika, sys, os, json
import pandas as pd
from hdfs import InsecureClient
import os, requests
from json import dump, dumps

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='theMusketeer')
    client_hdfs = InsecureClient('http://localhost:9870/', user='hadoop')

    dir = "/global"
    def callback(ch, method, properties, body):
        body = json.loads(body.decode())
        timestr = body["time"]
        data = body["data"]
        print(timestr)
        print(len(data))
        hdfs_path = dir + '/data-' + timestr + '.json'
        local_path = './subcribe/data-' + timestr + '.json'
        with open(local_path, 'w+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        status = client_hdfs.status(hdfs_path, strict=False)
        if not status:
            # client_hdfs.write(path, data=dumps(data), encoding='utf-8')
            client_hdfs.upload(hdfs_path, local_path)
        else:
            print("file " + hdfs_path + " already exists!")

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