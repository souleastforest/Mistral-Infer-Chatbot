import os
import logging
from logging import handlers
from datetime import time

from codestral_mamba.config.settings import settings


format_string = "%(asctime)s,%(levelname)s,%(pathname)s,%(module)s,%(funcName)s[%(lineno)d]:%(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(format_string, date_format)

def setup_log():
    appname = settings.appname

    logger_dir = os.path.join(settings.project_dir, "run", "logs")

    # 确保日志目录存在
    os.makedirs(logger_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置日志记录器的级别为 DEBUG

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 设置控制台处理器的级别为 DEBUG
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # info 级别日志文件处理器
    info_handler = create_log_handler(
        os.path.join(logger_dir, f"{appname}-info.log"),
        logging.INFO,
    )
    logger.addHandler(info_handler)

    # error 级别日志文件处理器
    error_handler = create_log_handler(
        os.path.join(logger_dir, f"{appname}-error.log"),
        logging.ERROR,
    )
    logger.addHandler(error_handler)

def create_log_handler(filename: str, level: int) -> handlers.TimedRotatingFileHandler:
    handler = handlers.TimedRotatingFileHandler(
        filename=filename,
        when="D",
        interval=1,
        backupCount=5,
        encoding="utf-8",
        atTime=time(0, 0),
        utc=True,
    )
    handler.suffix = "%Y-%m-%d.log"
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler