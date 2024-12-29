import datetime

import globals
from globals import global_state

# reminder函数是在main中通过监控调用fcc调用的
# 另一个remind_setter是经过responder检查后调用的主动程序
# 前者读取监控文档（或者变量？变量又得搞全局了）
# ！我想到了 可以为fcc指定一个不定作用备用参数，用于接收不同function的特定需求变量


def reminder(logger, chat_to_who, remind_message, role = "New"):
    for key,value in remind_message.items():
        if value[1] <= datetime.datetime.now():
            global_state.global_wx.SendMsg(msg=value[0], who=chat_to_who, at=key)
    return 0


if __name__ == "__main__":
    remind_message = {"目标0": ["未定义提醒0", 0], "目标1": ["未定义提醒1", 1]}
    for key, value in remind_message.items():
        print('msg=',value[0], 'who=',"测试", 'at=',key)

