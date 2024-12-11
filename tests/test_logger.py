import logging
from logging import Logger

from src.foundation_python.logger import load_log_config, format_log, logger_instance

def test_load_log_config():
    log_level, log_dir = load_log_config()
    assert log_level == 'INFO'
    assert log_dir == '/tmp/logs'

def test_format_log():
    result = format_log()
    assert isinstance(result, logging.Formatter)

def test_logger_instance():
    result = logger_instance('cv_test')
    assert isinstance(result, Logger)