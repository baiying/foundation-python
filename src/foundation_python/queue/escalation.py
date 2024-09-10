from queue_manager import QueueManager


class Escalation:
    """
    向中央队列回报任务执行结果
    """
    def __init__(self, queue_name):
        """
        :param queue_name: 回执队列名称
        """
        self.queue = QueueManager('central', queue_name)

    async def submit(self, task_id, status, data=None):
        """
        提交回执
        :param task_id: 任务ID
        :param status: 任务执行结果，取值：success/fail
        :param data: 回执中携带的数据
        :return:
        """
        await self.queue.add_job('escalation', {
            "task_id": task_id,
            "status": status,
            "data": data
        })

