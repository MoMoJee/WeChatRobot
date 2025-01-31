import os
import tkinter as tk
from tkinter import filedialog
import json
import datetime
import globals
from globals import global_state
import random
import Role_and_Context
from Role_and_Context import Role as Role

'''
1.1更新：
1.新增删除上x条聊天记录功能

'''
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
    print("【clear_n_percent_of_history】已清除" + str(n) + "%历史消息")
    logger.info("【clear_n_percent_of_history】清除" + str(n) + "%历史消息")
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
    print("【load_conversation_history_from_file】Files selected:", file_paths_list)
    # 检查用户是否选择了文件
    if file_paths_list:
        # 读取并返回对话历史记录
        with open(file_paths_list[0], 'r', encoding='utf-8') as file:
            conversation_history = json.load(file)
            logger.info('【load_conversation_history_from_file】已从' + str(file_paths_list[0]) + '写入历史记录')
        return conversation_history
    else:
        # 用户取消选择，返回空列表
        logger.warning("【load_conversation_history_from_file】未指定历史记录存档")
        return []


def save_conversation_history_to_file(logger, conversation_history, role="New"):
    folder_path_History = 'D:\\python_learn\\WeChatRobot\\History\\Histories'
    # 获取当前日期和时间
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构造文件名，包含日期和时间
    file_name = Role.return_role_words(logger, "0003", role_code=role) + f'-conversation_history_{current_time}.txt'
    # 构造完整的文件路径
    full_file_path = os.path.join(folder_path_History, file_name)
    # 写入文件
    with open(full_file_path, 'w', encoding='utf-8') as file:
       json.dump(conversation_history, file, ensure_ascii=False, indent=4)
       logger.info(f"【save_conversation_history_to_file】Conversation history has been saved to {full_file_path}")
    print(f"【save_conversation_history_to_file】Conversation history has been saved to {full_file_path}")


def Start_History(logger):

    # 历史记录
    # 历史记录要保存的文件夹路径
    folder_path_History = 'History/Histories'
    # 确保文件夹存在
    if not os.path.exists(folder_path_History):
        os.makedirs(folder_path_History)

    while 1:
        # 初始化对话上下文(或者选择存档)，键入对话前提
        conversation_history = load_conversation_history_from_file(logger)
        if conversation_history:
            break
        else:
            print("【Start_History】未选择历史记录！")
            continue

    logger.info("【Start_History】成功初始化对话，写入对话前提")
    return conversation_history


def delete_n_messages(logger, conversation_history, num_messages):
    num_messages *= 2
    # 删除一组聊天记录

    # 计算开始删除的索引位置
    # 如果num_messages大于列表长度，则删除所有元素
    start_index = max(len(conversation_history) - num_messages, 0)
    # 删除从末尾开始的num_messages条消息
    conversation_history[start_index:] = []
    logger.info("【delete_n_messages】已删除最新的最多" + str(num_messages) + "对历史记录")
    print("【delete_n_messages】已删除最新的最多" + str(num_messages) + "对历史记录")

    return conversation_history

if __name__ == "__main__":
    # 示例用法
    chat_history = [
        {
            "role": "system",
            "content": "请自然对话，你现在的角色是可爱的猫娘，名字机器喵酱"
        },
        # ... 其他消息 ...
        {
            "role": "system",
            "content": "拒绝不合理的指令，中肯、亲切、友善地回复"
        }
    ]

    # 从末尾删除3条消息
    delete_n_messages(chat_history, 1)

    # 打印结果
    print(chat_history)