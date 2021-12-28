# -*- coding:utf-8 -*-


"""
消费者
"""

import pickle
import traceback

from mq.mq import MQConnection, ExchangeChannel


# 创建MQ连接
mq = ExchangeChannel(MQConnection())


@mq.callback
def callback(channel, method, properties, message):
    try:
        print('[*] Waiting for logs. To exit press CTRL+C')
        msg = pickle.loads(message)
        print("消息内容:{}".format(msg))
    except Exception as e:
        traceback.print_exc()
        globalLog.error(f"Exception as {e} -> {traceback.format_exc()}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        channel.close(reply_text='callback func running Error')


if __name__ == '__main__':
    mq.listening(queue_name='test', exchange_name='test', routing_key='test', callback=callback)
