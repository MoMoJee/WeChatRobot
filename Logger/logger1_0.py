import os
import datetime
import logging
from pathlib import Path
import globals
from globals import global_state

def setup_logging(file_path,logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG

    # 创建一个handler，用于写入日志文件，并指定编码为utf-8
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # 设置文件日志级别为DEBUG

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)



    return logger

def start_logging(logger_name="new_logger",log_name="new-log_"):
    # 日志配置
    # 指定要保存的文件夹路径
    folder_path = 'D:\\python_learn\\WeChatRobot\\Logger\\logs'  # 替换为你的文件夹路径
    # 确保文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取当前时间并格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构造文件名，包含时间戳
    file_name = log_name + f'{current_time}.txt'
    # 构造完整的文件路径
    full_file_path = os.path.join(folder_path, file_name)
    global_state.global_log_file_path = full_file_path

    # 创建日志记录器
    logger = setup_logging(full_file_path,logger_name)

    return logger


if __name__ == '__main__':
    # 日志配置
    # 指定要保存的文件夹路径
    folder_path = 'logs'  # 替换为你的文件夹路径
    # 确保文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取当前时间并格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构造文件名，包含时间戳
    file_name = f'Kimi-MiaoJiang-log_{current_time}.txt'
    # 构造完整的文件路径
    full_file_path = os.path.join(folder_path, file_name)


    # 创建日志记录器
    logger = setup_logging(full_file_path)

