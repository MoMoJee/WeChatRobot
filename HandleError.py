import History
from History import History as History
from  globals import global_state
from Role_and_Context import Role

def handle_error(logger, e, role = 0):
    role_keyword = Role.return_role_words(logger, role_key="0001", role_code=role)
    # 将异常对象转换为字符串。我不会处理错误类型的e，这属于是解决不了错误就把错误绕开
    error_str = str(e)
    # 尝试从错误字符串中提取 'type' 和 'message'
    try:
        # 错误的开始和结束位置
        start = error_str.find("{'error':") + len("{'error':")
        end = error_str.find("}}", start)
        # 提取错误信息子字符串
        error_info = error_str[start:end]
        # 分割消息和类型
        parts = error_info.split("', 'type': '")
        message = parts[0].strip().strip("'")
        error_type = parts[1].strip().strip("'}").strip("}")
    except (ValueError, IndexError):
        # 如果提取失败，使用默认错误信息
        error_type = 'unknown_error'
        message = error_str
    cache_dialogue = Role.return_role_words(logger=logger, role_code=role, role_key="1000")
    # 根据错误类型返回相应的错误描述
    if error_type == 'content_filter':
        error_message = "喵酱不想回答啦~您的输入或生成内容可能包含不安全或敏感内容喵~"
    elif error_type == 'invalid_request_error':
        if "token length too long" in message:
            error_message = f"请求中的 tokens 长度过长，{role_keyword}记不住啦~请求不要超过模型 tokens 的最长限制喵~。"
            global_state.G_conversation_History = History.clear_n_percent_of_history(logger, global_state.G_conversation_History, 25)  # 调用清理函数，随机删除25%聊天数据
            logger.info("已删除25%历史记录")
            global_state.G_conversation_History.extend(cache_dialogue)
            logger.info("重申初始化")
            # 重申原始表述避免误删除
            # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
            # 保存对话历史到文件
            History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role)
        elif "exceeded G_model token limit" in message:
            error_message = f"呜呜 请求的 tokens 数和设置的 max_tokens 之和超过了模型规格长度喵~。让{role_keyword}休息一下啦~"
            global_state.G_conversation_History = History.clear_n_percent_of_history(logger, global_state.G_conversation_History, 25)  # 调用清理函数，随机删除25%聊天数据
            logger.info("已删除25%历史记录")
            global_state.G_conversation_History.extend(cache_dialogue)
            logger.info("重申初始化")
            # 重申原始表述避免误删除
            # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
            # 保存对话历史到文件
            History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role)
        elif "File size is zero" in message:
            error_message = f"没有告诉{role_keyword}任何信息啊~"
        elif "Invalid purpose" in message:
            error_message = "请求中的目的（purpose）不正确，当前只接受 'file-extract'，请修改后重新请求"
        else:
            error_message = "请求无效，通常是您请求格式错误或者缺少必要参数。话不说清楚喵~"
    elif error_type == 'invalid_authentication_error':
        error_message = "鉴权失败，请检查 API key 是否正确。"
    elif error_type == 'exceeded_current_quota_error':
        error_message = f"{role_keyword}饿了，小鱼干账户额度不足，请检查账户余额。"
    elif error_type == 'permission_denied_error':
        error_message = "您没有权限执行此操作。"
    elif error_type == 'resource_not_found_error':
        error_message = "找不到指定的资源或没有授权访问。"
    elif error_type == 'rate_limit_reached_error':
        error_message = "问得太快啦，请求触发了速率限制，请稍后再试喵~"
    elif error_type == 'engine_overloaded_error':
        error_message = f"当前并发请求过多喵~节点限流中~别急别急 {role_keyword}一个一个回答~"
    elif error_type == 'server_error':
        error_message = "内部错误，请联系管理员。"
    else:
        error_message = f"发生了一个未知错误: {message},{role_keyword}也不知道该怎么办了"

    return error_message
