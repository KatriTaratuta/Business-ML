import json
import pandas as pd
import pika
from datetime import datetime

# Лог-файл
LOG_FILE = './logs/metric_log.csv'

# Инициализация лог-файла
with open(LOG_FILE, 'w') as f:
    f.write('id,y_true,y_pred,absolute_error\n')

# Настройка очередей RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='features')
channel.queue_declare(queue='true_labels')
channel.queue_declare(queue='predictions')

# Хранилище сообщений
storage = {'y_true': {}, 'y_pred': {}}

def calculate_absolute_error(y_true, y_pred):
    return abs(y_true - y_pred)

def write_to_log(id, y_true, y_pred, error):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{id},{y_true},{y_pred},{error}\n")

def callback(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    
    if method.routing_key == 'true_labels':
        storage['y_true'][message_id] = message['body']
    elif method.routing_key == 'predictions':
        storage['y_pred'][message_id] = message['body']
    
    # Если данные готовы
    if message_id in storage['y_true'] and message_id in storage['y_pred']:
        y_true = storage['y_true'].pop(message_id)
        y_pred = storage['y_pred'].pop(message_id)
        error = calculate_absolute_error(y_true, y_pred)
        write_to_log(message_id, y_true, y_pred, error)
        print(f"Logged: ID={message_id}, y_true={y_true}, y_pred={y_pred}, error={error}")

channel.basic_consume(queue='true_labels', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='predictions', on_message_callback=callback, auto_ack=True)
print("Waiting for messages...")
channel.start_consuming()
