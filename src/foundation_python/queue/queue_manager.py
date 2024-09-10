from bullmq import Queue, Worker, Job
import redis.asyncio as redis
from queue_config import *
from redis import exceptions
from asyncio import Event


class QueueManager:
    def __init__(self, queue_type='central', queue_name='', opts=None):
        """
        指定队列的管理器
        :param queue_type: 队列类型，取值：central 中央队列，local 本地队列
        :param queue_name: 队列名称
        :param opts: 本地队列配置参数，当type=local时，该参数才生效。该参数中需要包含以下字段：
        host: 本地redis服务器地址
        port: 本地REDIS服务器端口
        db: 本地redis服务器数据库编号
        """
        self.queue = None
        self.client = None
        if queue_name == '':
            raise ValueError(f"未设置队列名称")
        self.queue_name = queue_name

        if queue_type == 'central':
            self.client = redis.Redis(
                decode_responses=True,
                host=CENTRAL_REDIS_HOST,
                port=CENTRAL_REDIS_PORT,
                db=CENTRAL_REDIS_DB
            )
        elif queue_type == 'local':
            if opts is None:
                raise ValueError(f"缺少本地队列配置信息")

            self.client = redis.Redis(
                decode_responses=True,
                host=opts['host'],
                port=opts['port'],
                db=opts['db']
            )
        else:
            raise ValueError(f"{queue_type} 是无效的队列类型值，队列类型值包括：central, local")

        retry = 0
        while retry < CONNECT_FAILED_RETRY:
            try:
                self.queue = Queue(queue_name, {
                    "connection": self.client,
                    "prefix": QUEUE_PREFIX
                })
            except exceptions.ConnectionError:
                retry += 1
                if retry > CONNECT_FAILED_RETRY:
                    print('连接消息队列失败')
                    raise Exception(f"连接 {queue_type} 消息队列失败，队列名称为：{queue_name}, 配置参数为：{opts}")

    async def add_job(self, job_name, job_data, opts):
        """
        向队列中添加新任务
        :param job_name: 任务名称
        :param job_data: 任务数据
        :param opts: 任务配置，参见BullMQ中任务配置项
        :return:
        """
        await self.queue.add(job_name, job_data, opts)

    async def start_worker(self, process_func):
        """
        启动工作进程消费任务
        :return:
        """
        stop_event = Event()

        def on_completed(job, result):
            pass

        def on_failed(job, err):
            pass

        worker = Worker(self.queue_name, process_func, {
            "connection": self.client,
            "prefix": QUEUE_PREFIX
        })

        try:
            await stop_event.wait()
        finally:
            await worker.close()
