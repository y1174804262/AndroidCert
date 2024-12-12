from loguru import logger


def create_log():
    # logger.remove(0)
    logger.add("../log_config/log_file_2.log", rotation="10 MB", level="DEBUG")
    print("日志框架已经创建")
    return logger
