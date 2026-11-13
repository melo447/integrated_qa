import os
import logging
from pathlib import Path

def setup_logger(log_file_path="logs/app.log"):
    """
    创建日志实例对象。
    :param log_file_path: 日志文件路径。默认是logs/app.log
    :return: 日志类实例对象。后续拿着直接用
    """

    # 0- 构建日志文件的路径
    real_file_path = Path(__file__).parent.parent / log_file_path

    # 1- 确保日志存放路径存在
    os.makedirs(name=os.path.dirname(real_file_path),exist_ok=True)

    # 2- 创建日志实例对象
    logger = logging.getLogger("EduRAG")
    logger.setLevel(logging.INFO)

    # 3- 控制台输出配置对象
    console_config = logging.StreamHandler()

    # 4- 文件输出配置对象
    file_config = logging.FileHandler(
        filename=real_file_path,
        mode="a",
        encoding="UTF-8"
    )

    # 5- 设置日志格式
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(module)s %(lineno)d - %(message)s")

    # 6- 控制台、文件使用相同的日志格式
    console_config.setFormatter(formatter)
    file_config.setFormatter(formatter)

    # 7- 将配置对象添加到日志实例对象中
    # not logger.handlers：避免往logger中重复添加配置项
    if not logger.handlers:
        logger.addHandler(file_config)
        logger.addHandler(console_config)

    # 8- 返回结果
    return logger


# 全局变量：也就是单例模式，目的是让整个项目共用一个对象，为了节省资源
if __name__ == '__main__':
    logger = setup_logger()

    logger.debug("这是一条debug日志")
    logger.info("这是一条info日志")
    logger.warning("这是一条warning日志")
    logger.error("这是一条error日志")
    logger.critical("这是一条critical日志")
