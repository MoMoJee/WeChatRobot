import os
import tkinter as tk
from tkinter import filedialog
import json
import datetime
import globals
from  globals import global_state
import random


def clear_n_percent_of_history(logger, history,n=25):
    # 计算需要移除的消息数量（列表长度的25%）
    divideNum = 100//n
    num_to_remove = max(1, len(history) // divideNum)  # 至少移除1条消息，避免除以0
    # 随机选择消息进行移除
    messages_to_remove = random.sample(history, num_to_remove)
    # 移除选中的消息
    for msg in messages_to_remove:
        if msg in history:
            history.remove(msg)
    print("已清除" + str(n) + "%历史消息")
    logger.info("已清除" + str(n) + "%历史消息")
    return history

def load_conversation_history_from_file(logger):
    # 创建一个Tkinter根窗口
    root = tk.Tk()
    # 创建一个Toplevel窗口并隐藏
    top = tk.Toplevel(root)
    top.withdraw()
    # 启动事件循环
    root.update()
    # 调用文件选择对话框，允许选择多个文件
    file_paths = filedialog.askopenfilenames()
    # 将返回的元组转换为列表
    file_paths_list = list(file_paths)
    # 关闭Tkinter根窗口
    root.destroy()
    print("Files selected:", file_paths_list)
    # 检查用户是否选择了文件
    if file_paths_list:
        # 读取并返回对话历史记录
        with open(file_paths_list[0], 'r', encoding='utf-8') as file:
            conversation_history = json.load(file)
            logger.info('已从' + str(file_paths_list[0]) + '写入历史记录')
        return conversation_history
    else:
        # 用户取消选择，返回空列表
        logger.warning("未指定历史记录存档")
        return []


def save_conversation_history_to_file(logger, conversation_history, role = "New"):
    folder_path_History = 'D:\\python_learn\\WeChatRobot\\History\\Histories'
    # 获取当前日期和时间
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构造文件名，包含日期和时间
    file_name = f'New-conversation_history_{current_time}.txt'
    # 构造完整的文件路径
    full_file_path = os.path.join(folder_path_History, file_name)
    # 写入文件
    with open(full_file_path, 'w', encoding='utf-8') as file:
       json.dump(conversation_history, file, ensure_ascii=False, indent=4)
       logger.info(f"Conversation history has been saved to {full_file_path}")
    print(f"Conversation history has been saved to {full_file_path}")


def Start_History(logger):

    # 历史记录
    # 历史记录要保存的文件夹路径
    folder_path_History = 'D:\\python_learn\\WeChatRobot\\History\\Histories'
    # 确保文件夹存在
    if not os.path.exists(folder_path_History):
        os.makedirs(folder_path_History)
    # 初始化对话上下文(或者选择存档)，键入对话前提
    conversation_history = load_conversation_history_from_file(logger)

    logger.info("成功初始化对话，写入对话前提")


    return conversation_history
