import pika
import json

class MessageBus:
    def __init__(self, host='rabbitmq'):
        self.host = host

    def publish(self, message: dict):
        try:
            # Kết nối tới RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            channel = connection.channel()

            # Đảm bảo hàng đợi tồn tại
            channel.queue_declare(queue='inventory_queue')

            # Gửi tin nhắn
            channel.basic_publish(
                exchange='',
                routing_key='inventory_queue',
                body=json.dumps(message)
            )

            print(f"Message sent to queue: {message}")

            # Đóng kênh và kết nối
            channel.close()
            connection.close()
        except Exception as e:
            print(f"Failed to send message: {e}")
            raise
