import logging
from logging.handlers import TimedRotatingFileHandler
from logger_config import LOG_DIR, LOG_LEVEL
from log_formatter import format_log


def logger_instance(name):
    """
    生成日志实例
    :param name: 日志实例名称
    :return: Logger
    """
    instance = logging.getLogger(name)
    instance.setLevel(LOG_LEVEL)
    # 控制台日志处理
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format_log())
    # 文件日志处理
    file_handler = TimedRotatingFileHandler(f'{LOG_DIR}/app.log', when='midnight', interval=1)
    file_handler.setFormatter(format_log())
    file_handler.suffix = '%Y%m%d'
    instance.addHandler(file_handler)
    return instance

