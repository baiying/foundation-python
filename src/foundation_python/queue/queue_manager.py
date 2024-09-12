from bullmq import Queue, Worker, Job
import redis.asyncio as redis
from redis import exceptions
from asyncio import Event
from ..util.common import load_global_config, load_local_config


class QueueManager:
    def __init__(self, queue_type='central', queue_name=''):
        """
        指定队列的管理器
        :param queue_type: 队列类型，取值：central 中央队列，local 本地队列
        :param queue_name: 队列名称
        """
        self.queue = None
        self.client = None
        self.global_config = load_global_config()
        self.local_config = load_local_config()

        if queue_name == '':
            raise ValueError(f"未设置队列名称")
        self.queue_name = queue_name

        if queue_type == 'central':
            self.client = redis.Redis(
                decode_responses=True,
                host=self.global_config['central_queue_setting']['host'],
                port=int(self.global_config['central_queue_setting']['port']),
                db=int(self.global_config['central_queue_setting']['db'])
            )
        elif queue_type == 'local':
            self.client = redis.Redis(
                decode_responses=True,
                host=self.local_config['local_queue_setting']['host'],
                port=int(self.local_config['local_queue_setting']['port']),
                db=int(self.local_config['local_queue_setting']['db'])
            )
        else:
            raise ValueError(f"{queue_type} 是无效的队列类型值，队列类型值包括：central, local")

        retry = 0
        connected = False
        while not connected and retry < self.global_config['queue_common_setting']['connect_failed_retry_times']:
            try:
                self.queue = Queue(queue_name, {
                    "connection": self.client,
                    "prefix": self.global_config['queue_common_setting']['prefix']
                })
                connected = True
            except exceptions.ConnectionError:
                retry += 1
                if retry > self.global_config['queue_common_setting']['connect_failed_retry_times']:
                    print('连接消息队列失败')
                    raise Exception(f"连接 {queue_type} 消息队列失败，队列名称为：{queue_name}")

    async def add_job(self, job_name, job_data, opts=None):
        """
        向队列中添加新任务
        :param job_name: 任务名称
        :param job_data: 任务数据
        :param opts: 任务配置，参见BullMQ中任务配置项
        :return:
        """
        if opts is None:
            await self.queue.add(job_name, job_data)
        else:
            await self.queue.add(job_name, job_data, opts)

    async def start_worker(self, func_process, func_completed=None, func_failed=None):
        """
        启动工作进程消费任务
        :return:
        """
        stop_event = Event()

        def on_completed(job, result):
            if func_completed is not None:
                func_completed(job, result)
            else:
                pass

        def on_failed(job, err):
            if func_failed is not None:
                func_failed(job, err)
            else:
                pass

        worker = Worker(self.queue_name, func_process, {
            "connection": self.client,
            "prefix": self.global_config['queue_common_setting']['prefix']
        })
        
        worker.on("completed", on_completed)
        worker.on("failed", on_failed)

        try:
            await stop_event.wait()
        finally:
            await worker.close()
