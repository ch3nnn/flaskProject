# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/8/11 19:06

import pika

HOST = 'localhost'  # rabbitmq服务地址
PORT = 5672  # 服务端口
USER = 'admin'  # 用户名
PASSWORD = 'admin'  # 密码


class MQConnection:

    def __init__(self, host=HOST, port=PORT, user=USER, password=PASSWORD, vhosts='test'):
        super(MQConnection, self).__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.vhosts = vhosts

        credentials = pika.PlainCredentials(username=self.user, password=self.password)

        parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhosts,
                credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)

    def close(self):
        if self.connection:
            self.connection.close()

    def channel(self):
        return self.connection.channel()


class MQChannel(object):

    def __init__(self, connection):
        super(MQChannel, self).__init__()
        self.mqc = connection
        self.channel = connection.channel()


class MQSender(MQChannel):

    def send(self, exchange='', routing_key='', message=None):
        """发送数据到MQ

        @param exchange: 交换器
        @param routing_key: 匹配key
        @param message: 发送信息数据
        """
        self.channel.exchange_declare(exchange=exchange, durable=True)
        self.channel.confirm_delivery()
        import pickle
        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=pickle.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print('Message was published')
        except:
            print('Message was returned')

        self.mqc.close()


if __name__ == '__main__':
    sender = MQSender(MQConnection())
    print("@@@@@@@@@@@@@@@@@@@@@@@@测试发送@@@@@@@@@@@@@@")
    sender.send(exchange='test', routing_key='test', message="hello world")
    print("@@@@@@@@@@@@@@@@@@@@@@@@发送成功@@@@@@@@@@@@@@")
