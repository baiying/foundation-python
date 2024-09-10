import logging


def format_log():
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    return formatter
