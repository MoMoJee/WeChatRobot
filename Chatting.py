import AIConnect
from globals import global_state
import HandleError as HandleError
import requests
from History import History as History
from Role_and_Context import Role
from datetime import datetime
import ollama




def chat_with_AI(logger, user_message, client, user_role, role = 0, retry_count=0):
    cache_dialogue = Role.return_role_words(logger=logger, role_code=role, role_key="1000")
    # 将用户的消息添加到对话历史中

    current_time = datetime.now()

    # 将当前时间格式化为字符串，格式为：年-月-日 时:分:秒
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    global_state.G_conversation_History.append({"role": user_role, "content": f'{time_str},{user_message}'})

    try:
        if global_state.G_model_code > 1000:
            completion = ollama.chat(
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
                temperature=1.3,
                max_tokens=200# 限制回复长度
            )

            # 将AI的回复添加到对话历史中
            global_state.G_conversation_History.append({"role": "assistant", "content": completion.choices[0].message.content})
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            global_state.G_Consumption += (prompt_tokens + completion_tokens)
            logger.info("【chat_with_AI】本轮对话上传的tokens数量：" + str(prompt_tokens))
            logger.info("【chat_with_AI】本轮对话返回的tokens数量：" + str(completion_tokens))
            logger.info("【chat_with_AI】本轮对话开销：" + str(prompt_tokens + completion_tokens) + "tokens，" + str(
                (prompt_tokens + completion_tokens) / 1000000 * 12) + "元")

            # 返回Kimi的回复
            if prompt_tokens > 7373:  # 创建tokens过载逻辑，占用90%以上时触发
                logger.warning('【chat_with_AI】剩余的上下文长度不足10%，当前占用tokens：' + str(prompt_tokens) + '，' + str(
                    int(prompt_tokens * 100 / 8192)) + "%")
                global_state.G_conversation_History = History.clear_n_percent_of_history(logger,
                                                                                         global_state.G_conversation_History,
                                                                                         25)  # 调用清理函数，随机删除25%聊天数据
                logger.info("【chat_with_AI】已删除25%历史记录")
                global_state.G_conversation_History.extend(cache_dialogue)
                logger.info("【chat_with_AI】重申初始化")
                # 重申原始表述避免误删除
                # 保存对话历史到文件。我为了方便，不加别的定时保存逻辑，只在90%占用时保存对话历史
                # 保存对话历史到文件
                History.save_conversation_history_to_file(logger, global_state.G_conversation_History)
                return completion.choices[0].message.content + Role.return_role_words(logger, role_code=role, role_key="2000")
            else:
                return completion.choices[0].message.content



    except Exception as e:
        global_state.G_error_code = 1
        logger.error(f'【chat_with_AI】{e}')
        if retry_count < 3:
            logger.info(f'【chat_with_AI】开始执行第{retry_count + 1}次重试')
            client = AIConnect.AIConnector(logger, choice=global_state.G_model_code, temp=False)
            return chat_with_AI(logger, user_message, client, user_role, role, retry_count + 1)
            # 这里的重试逻辑，主要是为了应对在CC中我已经修改了模型名称和模型，但是Client没变
            # 问题在于，即便这里重试成功，client下一次传入还是原始的状态
            # 根源在于我不想全局Client
            # 解决方案是加一个全局变量码指示这个状态，然后在Main函数中检查，True则在Main函数中再一次设置Client
            # 这个也可以用于别的错误检查，然后全部执行重连，包括微信等
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