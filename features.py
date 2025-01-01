import time
import random
from datetime import datetime
import json
import pika

# Пример данных 
X = [[random.random() for _ in range(5)] for _ in range(100)]  # Векторы признаков
y = [random.randint(0, 300) for _ in range(100)]  # Истинные метки

# Настройка очередей RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='features')
channel.queue_declare(queue='true_labels')

while True:
    random_row = random.randint(0, len(X) - 1)
    message_id = datetime.timestamp(datetime.now())
    
    # Отправка признаков
    message_X = {'id': message_id, 'body': X[random_row]}
    channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_X))
    
    # Отправка меток
    message_y = {'id': message_id, 'body': y[random_row]}
    channel.basic_publish(exchange='', routing_key='true_labels', body=json.dumps(message_y))
    
    print(f"Sent: {message_X} and {message_y}")
    time.sleep(5)  # Задержка
