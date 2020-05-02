import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread
from multiprocessing import JoinableQueue


class Shop:
    def __init__(self, maxsize=10):
        self.raw_queue = Queue()
        self.product_queue = JoinableQueue(maxsize=maxsize)

    # def set_producer(self, producer_func):
    #     self.producer_func = producer_func

    # def set_consumer(self, consumer_func, callback_func=None):
    #     self.consumer_func = consumer_func
    #     self.callback_func = callback_func

    def set_tasks(self, tasks):
        for task in tasks:
            self.raw_queue.put(task)

    def consumer_func(self):
        return

    def producer_func(self):
        return

    def on_finish(self):
        pass

    def producer(self):
        while True:
            product = self.producer_func(self.raw_queue)
            if isinstance(product, list):
                [self.product_queue.put(p) for p in product]
            else:
                self.product_queue.put(product)
            # raw = self.raw_queue.get()
            # if raw == '_finished':
            #     break
            # result = self.producer_func(raw, self.raw_queue)
            # if result:
            #     self.product_queue.put(result)

    def consumer(self, max_workers=10, sleep_time=1):
        thread_status = {
            'submitted': 0,
            'finished': 0
        }
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                shopping = \
                    thread_status['submitted'] - \
                    thread_status['finished']

                thread_nowait = max_workers >= shopping
                thread_empty = shopping == 0
                queue_empty = \
                    self.raw_queue.empty() and self.product_queue.empty()
                if queue_empty and thread_empty:
                    self.raw_queue.put('_finished')
                    self.on_finish(self)
                    break
                elif not thread_nowait:
                    time.sleep(sleep_time)
                else:

                    def callback(res):
                        if self.callback_func:
                            self.callback_func(res, self.raw_queue)
                        thread_status['finished'] += 1
                        self.product_queue.put('_refresh')

                    task = self.product_queue.get()

                    if task == '_refresh':
                        continue
                    thread_status['submitted'] += 1
                    future = self.consumer_func(executor, task)
                    future.add_done_callback(callback)

    def run(self, max_workers=10, sleep_time=1):
        producer_thread = Thread(target=self.producer)
        consumer_thread = Thread(
            target=self.consumer,
            args=(max_workers, sleep_time)
        )
        producer_thread.start()
        consumer_thread.start()


# if __name__ == '__main__':
#     import random
#     r = {'successed': [], 'failed': []}

#     def producer(i, raw_queue):
#         print('{} 生产者启动'.format(i))
#         time.sleep(0.1)
#         print('{} 生产者结束'.format(i))
#         return i, i**2

#     def consumer(executor, i):
#         print('{} 消费者启动'.format(i))

#         def a():
#             time.sleep(2)
#             return i
#         future = executor.submit(a)
#         print('{} 消费者结束'.format(i))
#         return future

#     def callback(res, raw_queue):
#         result = res.result()
#         if random.random() < 0.5:
#             r['failed'].append(result[0])
#             raw_queue.put(result[0])
#         else:
#             r['successed'].append(result[0])

#     def on_finish(shop):
#         print(r)

#     shop = Shop()
#     shop.set_tasks(range(10))
#     shop.set_producer(producer)
#     shop.set_consumer(consumer, callback)
#     shop.set_finish(on_finish)
#     shop.run()
