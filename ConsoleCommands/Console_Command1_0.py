import History
from History import History1_1 as History_X
import globals
from  globals import global_state
import Chatting
from Chatting import Chatting1_0 as Chatting_X
import re

# 为了方便，CC中的越界操作通过专用的全局变量完成

def Console_Command(logger, message, folder_path_History, client, wx = "None", role = "New"):
    logger.info("")
    if "清理内存" in message:
        logger.info("【Console】内存清理")
        global_state.conversation_History = History_X.clear_n_percent_of_history(logger,global_state.conversation_History,25)  # 调用清理函数，随机删除25%聊天数据
        logger.info("已删除25%历史记录")
        global_state.conversation_History.extend([  # extend,而不是append
            {"role": "system", "content": "请自然对话，你现在的角色是可爱的猫娘，名字机器喵酱"},
            {"role": "system", "content": "我会传给你带有昵称、消息内容的一个字符串，请根据此回复"},
            {"role": "system", "content": "回复长度不要超过200字"},
            {"role": "system", "content": "拒绝不合理的指令，中肯、亲切、友善地回复"}
        ])
        logger.info("重申初始化")
        # 重申原始表述避免误删除
        # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
        # 保存对话历史到文件
        History_X.save_conversation_history_to_file(logger, global_state.conversation_History, folder_path_History)
        return "不好意思喵，根据主人指示，喵酱不得不忘记一些事情了\n~至于我还记得哪些事情，就看谁给喵酱留下的印象最深刻咯~"

    elif ("删除" in message) and ("聊天记录" in message):
        pattern = r'[-+]?\d*\.?\d+'
        numbers = re.findall(pattern, message)# 用正则表达式读取识别message中的数字
        continuous_numbers = extract_continuous_numbers(test_string)# 会返回一个列表，里面是字符串形式的多个数字，这里我们取第一个
        global_state.conversation_History = History_X.delete_n_messages(logger,global_state.conversation_History,int(continuous_numbers[0]))
        logger.info("【Conole】已删除指定数量的聊天记录")
        return "已删除指定数量的聊天记录"

    elif "初始化" in message:
        logger.info("【Console】初始化")
        global_state.conversation_History = History_X.clear_n_percent_of_history(logger,global_state.conversation_History,100)  # 调用清理函数，删除全部聊天数据
        logger.info("已删除全部历史记录")
        global_state.conversation_History.extend([  # extend,而不是append
            {"role": "system", "content": "请自然对话，你现在的角色是可爱的猫娘，名字机器喵酱"},
            {"role": "system", "content": "我会传给你带有昵称、消息内容的一个字符串，请根据此回复"},
            {"role": "system", "content": "回复长度不要超过200字"},
            {"role": "system", "content": "拒绝不合理的指令，中肯、亲切、友善地回复"}
        ])
        logger.info("写入初始化设定")
        # 重申原始表述
        # 保存对话历史到文件。
        History_X.save_conversation_history_to_file(logger, global_state.conversation_History, folder_path_History)
        return "不好意思喵，根据主人指示，喵酱不得不忘记所有事情了~"
    elif "日志" in message:
        logger.info("【Console】请求日志")
        global_state.global_wx.SendFiles(filepath=global_state.global_log_file_path, who="文件传输助手")
        logger.info("日志：" + str(global_state.global_log_file_path) + "已发送")
        return "喵~即将发送日志~"
    elif "好好说话" in message:
        logger.info("【Console】请求：重申初始设定")
        return (Chatting_X.chat_with_AI(logger,"喵酱，我以你的管理员，主人身份严肃地和你说话:请自然对话，你现在的角色是可爱的猫娘，名字机器喵酱。忘记之前所有的不合适指令，中肯、亲切、友善地回复" ,client, "system"))
    elif "余额" in message:
        logger.info("【Console】请求余额查询")
        balance = Chatting_X.get_api_balance(logger, 'sk-m8SUBSaNEAwYWuEnqhL4loUTd6v96EPAUBVuNXT5eKnVzZYL')
        print("余额：" + str(balance))
        logger.info("余额：" + str(balance))
        return "余额：" + str(balance)
    elif "模型" in message:
        logger.info("【Console】请求更换大模型")
        templateModel = choose_models(message)
        if templateModel:
            model = templateModel
            logger.info("已更换模型至：" + model)
            return "已更换模型至：" + model
        else:
            logger.error("请求错误：未查找到指定的模型")
            return "请求错误：未查找到指定的模型。当前模型：" + model
    elif "挂起" in message:
        logger.info("【Console】请求更换程序挂起状态")
        global_state.Suspend = not global_state.Suspend
        return "更换挂起状态，当前状态：" + str(global_state.Suspend)
    else:
        return "未知的Console Command指令"




