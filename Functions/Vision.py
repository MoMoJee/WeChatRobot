import os
import base64
from globals import global_state
from openai import OpenAI
import HandleError as HandleError
from History import History as History

def vision(logger, user_message, client, user_role, image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    # 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
    image_url = f"data:image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"

    new_vision_message = [
                    {
                        "type": "image_url",  # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                        "image_url": {
                            "url": image_url,
                        },
                    },
                    {
                        "type": "text",
                        "text": user_message,  # <-- 使用 text 类型来提供文字指令，例如“描述图片内容”
                    },
                ]


    # 将用户的消息添加到对话历史中
    global_state.conversation_History.append({"role": user_role, "content": new_vision_message})

    # 调用Kimi API进行聊天
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k-vision-preview",
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
            History.save_conversation_history_to_file(logger, global_state.conversation_History)
            return completion.choices[0].message.content + "\n还有就是，不好意思喵，喵酱的上下文存储快要满了，不得不忘记一些事情了\n~至于我还记得哪些事情，就看谁给喵酱留下的印象最深刻咯~"
        else:
            return completion.choices[0].message.content
    except Exception as e:
        logger.error(e)
        return HandleError.handle_error(logger, e)  # 调用错误处理函数，返回错误类型







if __name__ == "__main__":
    client = OpenAI(
        api_key="sk-nudIQU6wuIIKeztAZTssRZuGILtxgjEpluHZBCKKfChvHgWu",
        base_url="https://api.moonshot.cn/v1",
    )

    # 在这里，你需要将 kimi.png 文件替换为你想让 Kimi 识别的图片的地址
    image_path = "D:\python_learn\WeChatRobot\wxauto文件\微信图片_20250115184048856090.jpg"

    with open(image_path, "rb") as f:
        image_data = f.read()

    # 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
    image_url = f":image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"

    completion = client.chat.completions.create(
        model="moonshot-v1-8k-vision-preview",
        messages=[
            {"role": "system", "content": "你是 Kimi。"},
            {
                "role": "user",
                # 注意这里，content 由原来的 str 类型变更为一个 list，这个 list 中包含多个部分的内容，图片（image_url）是一个部分（part），
                # 文字（text）是一个部分（part）
                "content": [
                    {
                        "type": "image_url",  # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                        "image_url": {
                            "url": image_url,
                        },
                    },
                    {
                        "type": "text",
                        "text": "请描述图片的内容。",  # <-- 使用 text 类型来提供文字指令，例如“描述图片内容”
                    },
                ],
            },
        ],
    )

    print(completion.choices[0].message.content)