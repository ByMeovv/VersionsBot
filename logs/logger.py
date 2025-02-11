import logging
import sys
import os


class CustomFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname.lower()
        if level == 'info':
            color = '\x1b[32m'  # Green
        elif level == 'debug':
            color = '\x1b[34m'  # Blue
        elif level == 'warning':
            color = '\x1b[33m'  # Yellow
        elif level == 'error':
            color = '\x1b[31m'  # Red
        elif level == 'critical':
            color = '\x1b[41m\x1b[37m'  # White on red background
        else:
            color = ''

        reset_color = '\x1b[0m'

        record.color_level = f'{color}{record.levelname}{reset_color}'
        return super().format(record)

def _get_logger(name, filename=None, console=True, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = CustomFormatter('%(asctime)s - %(name)s - %(color_level)s - %(message)s')

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


log = _get_logger(__name__, filename='app.log', console=True, level=logging.DEBUG)