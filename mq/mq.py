# -*- coding:utf-8 -*-


"""
MQ封装类
"""

from functools import wraps
import traceback
import pika


class MQConnection(object):
    """连接rabbitMQ"""

    def __init__(self, host="localhost", port=5672, user="admin", password="admin", vhosts='test'):
        """默认/虚拟主机"""
        super(MQConnection, self).__init__()
        self.host = host
        self.port = port
        self.name = user
        self.password = password
        self.vhosts = vhosts

        # 凭证
        credentials = pika.PlainCredentials(self.name, self.password)
        # 连接参数
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhosts,
            credentials=credentials,
            # heartbeat=0,  # 关闭心跳检测  消息处理时间过长导致与MQ断开连接
        )
        self.connection = pika.BlockingConnection(parameters)

    def close(self):
        if self.connection:
            self.connection.close()

    def channel(self):
        return self.connection.channel()


class MQChannel(object):
    """MQChannel文档提示"""

    def __init__(self, connection):
        """
        初始化
        :param connection: mq实例对象
        """
        super(MQChannel, self).__init__()
        self.mqc = connection
        self.channel = connection.channel()


class ExchangeChannel(MQChannel):
    """1对多路由匹配信道"""

    def send(self, exchange='default_exchange', routing_key='default_route', message='send ok'):
        """往mq交换机发送消息"""
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

    def listening(self, queue_name='default_queue', exchange_name='default_exchange',
                  routing_key='default_route', callback=None):
        """
        监听队列里的消息, 优先启动
        """
        # 创建exchange并设置类型
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=True
        )
        print("消费者连接MQ成功")

        # 指定死信队列配置 创建死信队列脚本 path: mq/DLXQueueScript.py
        arguments = {"x-dead-letter-exchange": "dlx.financial_news", "x-dead-letter-routing-key": "dlx"}
        # durable 持久化
        # auto_delete 是否自动删除queue 当还一个消费者断开连接
        # 切换到指定的队列中,如果队列不存在,则创建
        self.channel.queue_declare(
            queue=queue_name, durable=True, exclusive=False, auto_delete=False, arguments=arguments
        )
        # 绑定交换器和队列
        self.channel.queue_bind(
            exchange=exchange_name,
            routing_key=routing_key,
            queue=queue_name
        )

        # 在处理并确认上一条消息之前，不要将新消息发送给消费者
        # 而是将其分派给不忙的下一个工作程序 防止消息积压
        self.channel.basic_qos(prefetch_count=1)

        if not callback:
            callback = self.__callback

        # 调用回调函数处理消息数据
        # no_ack=False 设置为消息处理完毕后,消费者必须明确告知rabbitMQ server已经处理完毕
        # 否则rabbitMQ server将视为消息处理失败,把该消息重新放回到队列当中
        self.channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=False)
        try:
            # 消费者阻塞监听
            self.channel.start_consuming()
        except:
            traceback.print_exc()

    @staticmethod
    def __callback(channel, method, properties, message):
        """回调函数,处理从rabbitmq中取出的消息"""
        print(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)  # 手动发送ack回执消息

    @staticmethod
    def callback(callback_func):
        """回调函数装饰器"""
        @wraps(callback_func)
        def wrapper(channel, method, properties, message, *args, **kwargs):

            callback_func(channel, method, properties, message, *args, **kwargs)
            # 手动通知rabbitMQ server已经对消息处理完毕,可以释放掉保存的这个消息资源
            channel.basic_ack(delivery_tag=method.delivery_tag)
        return wrapper


if __name__ == '__main__':
    # TODO 测试消息
    # 此数据较多
    msg = {
        'start_time': '1577355239', 'collection_name': 'sy_news_hangye_chinagas_raw',
        'end_time': '1577357134', 'spider_name': 'hangye_chinagas_news'
    }

    # 此数据较少
    # msg = {
    #     'collection_name': 'sy_news_finance_caijing_raw', 'end_time': '1577773335', 'start_time': '1577773316',
    #     'spider_name': 'caijing_caijing_hongguan'
    # }

    mq = ExchangeChannel(MQConnection())
    mq.send(exchange='financial_news', routing_key='fn', message=msg)
