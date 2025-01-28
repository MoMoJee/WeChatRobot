import History
from History import History as History
from globals import global_state
import Chatting as Chatting
import re
from Role_and_Context import Role
import AIConnect

# 为了方便，CC中的越界操作通过专用的全局变量完成

def Console_Command(logger, message, folder_path_History, client, wx = "None", role = 0):
    cache_dialogue = Role.return_role_words(logger=logger, role_code=role, role_key="1000")
    if "清理内存" in message:
        logger.info("【Console】内存清理")
        global_state.G_conversation_History = History.clear_n_percent_of_history(logger, global_state.G_conversation_History, 25)  # 调用清理函数，随机删除25%聊天数据
        logger.info("已删除25%历史记录")
        global_state.G_conversation_History.extend(cache_dialogue)
        logger.info("重申初始化")
        # 重申原始表述避免误删除
        # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
        # 保存对话历史到文件
        History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role)
        return Role.return_role_words(logger, role_code=role, role_key="2000")

    elif ("删除" in message) and ("聊天记录" in message):
        pattern = r'[-+]?\d*\.?\d+'
        continuous_numbers = re.findall(pattern, message)# 用正则表达式读取识别message中的数字# 会返回一个列表，里面是字符串形式的多个数字
        if continuous_numbers:
            global_state.G_conversation_History = History.delete_n_messages(logger, global_state.G_conversation_History, int(continuous_numbers[0]))#这里我们取第一个
            logger.info("【Console】已删除指定数量的聊天记录")
            return "已删除指定数量的聊天记录"
        else:# 如果是空列表，会返回[]
            logger.warning("【Console】未指定要删除的聊天记录数量")
            return "未指定要删除的聊天记录数量"


    elif "初始化" in message:
        logger.info("【Console】初始化")
        global_state.G_conversation_History = History.clear_n_percent_of_history(logger, global_state.G_conversation_History, 100)  # 调用清理函数，删除全部聊天数据
        logger.info("已删除全部历史记录")
        global_state.G_conversation_History.extend(cache_dialogue)
        logger.info("写入初始化设定")
        # 重申原始表述
        # 保存对话历史到文件。
        History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role)
        return Role.return_role_words(logger, role_code=role, role_key="2001")
    elif "日志" in message:
        logger.info("【Console】请求日志")
        global_state.G_wx.SendFiles(filepath=global_state.G_global_log_file_path, who="文件传输助手")
        logger.info("日志：" + str(global_state.G_global_log_file_path) + "已发送")
        return Role.return_role_words(logger, role_code=role, role_key="2002")
    elif "好好说话" in message:
        logger.info("【Console】请求：重申初始设定")
        return Chatting.chat_with_AI(logger, Role.return_role_words(logger, role_code=role, role_key="2003"), client, "system", role=role)
    elif "余额" in message:
        logger.info("【Console】请求余额查询")
        balance = Chatting.get_api_balance(logger, AIConnect.read_api_key('AISetting.json', logger, cache_choice=2))
        # 暂时只写了kimi的余额查询
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
        global_state.G_Suspend = not global_state.G_Suspend
        return "更换挂起状态，当前状态：" + str(global_state.G_Suspend)
    else:
        return "未知的Console Command指令"




