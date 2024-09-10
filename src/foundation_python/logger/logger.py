import logging
from logging.handlers import TimedRotatingFileHandler
from logger_config import LOG_DIR, LOG_LEVEL
from log_formatter import format_log


class Logger:
    def __init__(self, name='app_logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LOG_LEVEL)

        # 控制台日志处理
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format_log())
        self.logger.addHandler(console_handler)

        # 文件日志处理
        file_handler = TimedRotatingFileHandler(f'{LOG_DIR}/app.log', when='midnight', interval=1)
        file_handler.setFormatter(format_log())
        file_handler.suffix = '%Y%m%d'
        self.logger.addHandler(file_handler)

    def log(self, level, message):
        if level.lower() == 'info':
            self.logger.info(message)
        elif level.lower() == 'warn':
            self.logger.warning(message)
        elif level.lower() == 'error':
            self.logger.error(message)


