from src.foundation_python.queue.queue_manager import QueueManager

def test_queue():
    queue = QueueManager('central', 'test')
    assert hasattr(queue, 'add_job')
