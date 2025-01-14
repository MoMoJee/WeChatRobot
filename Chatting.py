from  globals import global_state
import HandleError as HandleError
import requests
from History import History as History

def chat_with_AI(logger, user_message, client, user_role, retry_count=0):

    # 将用户的消息添加到对话历史中
    global_state.conversation_History.append({"role": user_role, "content": user_message})

    # 调用Kimi API进行聊天
    try:
        completion = client.chat.completions.create(
            model=global_state.model,  # 你可以根据需要选择不同的模型规格
            messages=global_state.conversation_History,
            temperature=0.3,
            max_tokens=200# 限制回复长度

        )

        # 将Kimi的回复添加到对话历史中
        global_state.conversation_History.append({"role": "assistant", "content": completion.choices[0].message.content})
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        global_state.Comsumption += (prompt_tokens + completion_tokens)
        logger.info("本轮对话上传的tokens数量：" + str(prompt_tokens))
        logger.info("本轮对话返回的tokens数量：" + str(completion_tokens))
        logger.info("本轮对话开销：" + str(prompt_tokens + completion_tokens) + "tokens，" + str(
            (prompt_tokens + completion_tokens) / 1000000 * 12) + "元")

        # 返回Kimi的回复
        if prompt_tokens > 7373:  # 创建tokens过载逻辑，占用90%以上时触发
            logger.warning('剩余的上下文长度不足10%，当前占用tokens：' + str(prompt_tokens) + '，' + str(
                int(prompt_tokens * 100 / 8192)) + "%")
            global_state.conversation_History = History.clear_n_percent_of_history(logger,
                                                                                   global_state.conversation_History,
                                                                                   25)  # 调用清理函数，随机删除25%聊天数据
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
            History.save_conversation_history_to_file(logger, global_state.conversation_History, folder_path_History)
            return completion.choices[0].message.content + "\n还有就是，不好意思喵，喵酱的上下文存储快要满了，不得不忘记一些事情了\n~至于我还记得哪些事情，就看谁给喵酱留下的印象最深刻咯~"
        else:
            return completion.choices[0].message.content
    except Exception as e:
        logger.error(e)
        return HandleError.handle_error(logger, e)  # 调用错误处理函数，返回错误类型



def get_api_balance(logger, api_key):
    # 替换为你的API端点和API密钥
    api_endpoint = "https://api.moonshot.cn/v1/users/me/balance"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    logger.info("API余额查询连接成功")

    try:
        response = requests.get(api_endpoint, headers=headers)
        # 检查响应码是否为200
        if response.status_code == 200:
            logger.info("获取到API响应")
            balance_info = response.json()
            return balance_info['data']['available_balance']
        else:
            logger.error("请求失败，状态码：" , + str(response.status_code))
            return "请求失败，状态码：" + str(response.status_code)
    except requests.RequestException as e:
        logger.error(f"请求失败：{e}")
        return f"请求失败：{e}"