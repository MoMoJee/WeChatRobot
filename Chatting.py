from globals import global_state
import HandleError as HandleError
import requests
from History import History as History
from Role_and_Context import Role
from datetime import datetime





def chat_with_AI(logger, user_message, client, user_role, role = 0, retry_count=0):
    cache_dialogue = Role.return_role_words(logger=logger, role_code=role, role_key="1000")
    # 将用户的消息添加到对话历史中

    current_time = datetime.now()

    # 将当前时间格式化为字符串，格式为：年-月-日 时:分:秒
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    global_state.G_conversation_History.append({"role": user_role, "content": f'{time_str},{user_message}'})

    try:
        if global_state.G_model_code > 1000:
            completion = client.chat(
                model=global_state.G_model,
                messages=global_state.G_conversation_History,
            )
            # 将AI的回复添加到对话历史中
            global_state.G_conversation_History.append(
                {"role": "assistant", "content": completion['message']['content']})
            return completion['message']['content']

        else:
            completion = client.chat.completions.create(
                model=global_state.G_model,  # AIConnect函数会更改这个
                messages=global_state.G_conversation_History,
                temperature=0.3,
                max_tokens=200# 限制回复长度

            )

            # 将AI的回复添加到对话历史中
            global_state.G_conversation_History.append({"role": "assistant", "content": completion.choices[0].message.content})
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            global_state.G_Consumption += (prompt_tokens + completion_tokens)
            logger.info("本轮对话上传的tokens数量：" + str(prompt_tokens))
            logger.info("本轮对话返回的tokens数量：" + str(completion_tokens))
            logger.info("本轮对话开销：" + str(prompt_tokens + completion_tokens) + "tokens，" + str(
                (prompt_tokens + completion_tokens) / 1000000 * 12) + "元")

            # 返回Kimi的回复
            if prompt_tokens > 7373:  # 创建tokens过载逻辑，占用90%以上时触发
                logger.warning('剩余的上下文长度不足10%，当前占用tokens：' + str(prompt_tokens) + '，' + str(
                    int(prompt_tokens * 100 / 8192)) + "%")
                global_state.G_conversation_History = History.clear_n_percent_of_history(logger,
                                                                                         global_state.G_conversation_History,
                                                                                         25)  # 调用清理函数，随机删除25%聊天数据
                logger.info("已删除25%历史记录")
                global_state.G_conversation_History.extend(cache_dialogue)
                logger.info("重申初始化")
                # 重申原始表述避免误删除
                # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
                # 保存对话历史到文件
                History.save_conversation_history_to_file(logger, global_state.G_conversation_History)
                return completion.choices[0].message.content + Role.return_role_words(logger, role_code=role, role_key="2000")
            else:
                return completion.choices[0].message.content



    except Exception as e:
        logger.error(e)
        return HandleError.handle_error(logger, e, role=role)  # 调用错误处理函数，返回错误类型



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