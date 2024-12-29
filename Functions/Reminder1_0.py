import datetime

import globals
from globals import global_state




def reminder(logger, chat_to_who, remind_message ={"目标0" : ["未定义提醒0", 0], "目标1" :["未定义提醒1", 0]}, role = "New"):
    for key,value in remind_message.items():
        if value[1] <= datetime.datetime.now():
            wx.SendMsg(msg=value[0], who=chat_to_who, at=key)
    global_state.global_wx.SendMsg()
    return 0


if __name__ == "__main__":
    remind_message = {"目标0": ["未定义提醒0", 0], "目标1": ["未定义提醒1", 1]}
    for key, value in remind_message.items():
        print('msg=',value[0], 'who=',"测试", 'at=',key)

