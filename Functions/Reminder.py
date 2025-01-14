import datetime

import globals
from globals import global_state

# reminder函数是在main中通过监控调用fcc调用的
# 另一个remind_setter是经过responder检查后调用的主动程序
# 前者读取监控文档（或者变量？变量又得搞全局了）
# ！我想到了 可以为fcc指定一个不定作用备用参数，用于接收不同function的特定需求变量


import datetime


def reminder(logger, chat, role="New"):
    filename = 'D:\\python_learn\\WeChatRobot\\Functions\\remind.txt'
    # 读取文件并解析为字典
    remind_message = parse_remind_file(filename)

    # 创建一个新的字典来存储更新后的提醒信息
    updated_remind_message = remind_message.copy()  # 复制原字典，避免修改原字典
    successful_remind = 1
    change_or_not = 0

    # 遍历提醒消息字典
    for key, value in remind_message.items():
        message, time_obj, remind_type = value
        if time_obj <= datetime.datetime.now():
            logger.info("【reminder】已到达某个指定的提醒时间")

            if remind_type == '0':
                # 不提醒，跳过
                logger.info("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "处于禁用状态，提醒取消")
                continue

            else:
                print('msg=', message, 'at=', key, value[1])
                try:
                    chat.SendMsg(msg=message, at=key)
                    logger.info("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "提醒已发送")
                except:
                    logger.error("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "提醒发送失败，请检查监听状态")
                    successful_remind = 0
                    break

                # 根据提醒类型更新时间或删除提醒
                if remind_type == '1':
                    # 单次提醒，提醒一次后标记为0
                    updated_remind_message[key] = [message, time_obj, '0']
                    change_or_not = 1
                    logger.info("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "这一提示已被修改为禁用")
                elif remind_type == '2':
                    updated_time = time_obj + datetime.timedelta(days=1)
                    logger.info("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "这一提示已被延后一天")
                    updated_remind_message[key] = [message, updated_time, remind_type]
                    change_or_not = 1
                elif remind_type == '3':
                    updated_time = time_obj + datetime.timedelta(hours=1)
                    logger.info("【reminder】msg=" + message + 'at=' + key + str(value[1]) + "这一提示已被延后一小时")
                    updated_remind_message[key] = [message, updated_time, remind_type]
                    change_or_not = 1
    if change_or_not:
        # 将更新后的提醒信息写回文件
        write_remind_file(updated_remind_message, filename)
        logger.info("【reminder】新的提醒文件已覆盖")

    if successful_remind:
        return 1
    else:
        return 0


def parse_remind_file(filename):
    remind_message = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split("; ")
            if len(parts) == 4:
                key, message, time_str, remind_type = parts
                time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                remind_message[key] = [message, time_obj, remind_type]
    return remind_message


def write_remind_file(remind_message, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for key, value in remind_message.items():
            message, time_obj, remind_type = value
            time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{key}; {message}; {time_str}; {remind_type}\n")


# 假设chat对象和logger对象已经定义
# reminder(logger, chat)


if __name__ == "__main__":
    remind_message = parse_remind_file("remind.txt")
    print(remind_message)
    for key, value in remind_message.items():
        print('msg=', value[0], 'at=', key, value[1])
    print("-----")


