import os
import base64
from globals import global_state
from openai import OpenAI
import HandleError as HandleError
import AIConnect
import copy
import ollama


def vision(logger, user_message, user_role, image_path, role=0):
    # 这是一个历史遗留。在只用kimi的情况下，将client传入是没问题的。但现在支持多模型切换，而vision只支持kimi，这就导致无论如何都需要在这里重新连接kimi的API，client的传入就不需要了
    choice = 3
    client = AIConnect.AIConnector(logger, choice=choice, temp=True)
    with open(image_path, "rb") as f:
        image_data = f.read()


    if choice > 1000:
        new_vision_message = {
            'role': user_role,
            'content': user_message,
            'images': [image_path]
        }
        message_without_vision = [
            {
                "role": "system",
                "content": "你收到一张图片"
            },
            {
                "role": user_role,
                "content": user_message
            }
        ]

        # 将用户的消息添加到对话历史中，由于vision模型接口不兼容其他模型，这里使用临时历史记录，全局的普通记录则只作描述，不放图。这也可以省点钱

        # 创建一个副本，这个copy方式第一次听说
        vision_temp_conversation_history = copy.copy(global_state.G_conversation_History)

        # 修改副本，不会影响原始列表
        vision_temp_conversation_history.append(new_vision_message)

        global_state.G_conversation_History.append(message_without_vision[0])
        global_state.G_conversation_History.append(message_without_vision[1])


        completion = ollama.chat(
            model=AIConnect.parse_AI_Setting_json(logger, choice)["model"],
            messages=vision_temp_conversation_history,
        )
        # 将AI的回复添加到对话历史中
        global_state.G_conversation_History.append(
            {"role": "assistant", "content": completion['message']['content']})
        return completion['message']['content']


    else:
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

        message_without_vision = [
            {
                "role": "system",
                "content": "你收到一张图片"
            },
            {
                "role": user_role,
                "content": user_message
            }
        ]



        # 将用户的消息添加到对话历史中，由于vision模型接口不兼容其他模型，这里使用临时历史记录，全局的普通记录则只作描述，不放图。这也可以省点钱

        # 创建一个副本，这个copy方式第一次听说
        vision_temp_conversation_history = copy.copy(global_state.G_conversation_History)

        # 修改副本，不会影响原始列表
        vision_temp_conversation_history.append({"role": user_role, "content": new_vision_message})


        global_state.G_conversation_History.append(message_without_vision[0])
        global_state.G_conversation_History.append(message_without_vision[1])

        # 调用Kimi API进行聊天
        try:
            completion = client.chat.completions.create(
                model=AIConnect.parse_AI_Setting_json(logger, choice)["model"],
                messages=vision_temp_conversation_history,
                temperature=0.3,
                max_tokens=200# 限制回复长度

            )

            # 将Kimi的回复添加到对话历史中
            global_state.G_conversation_History.append({"role": "assistant", "content": completion.choices[0].message.content})
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            global_state.G_Consumption += (prompt_tokens + completion_tokens)
            logger.info("【Vision】本轮对话上传的tokens数量：" + str(prompt_tokens))
            logger.info("【Vision】本轮对话返回的tokens数量：" + str(completion_tokens))
            logger.info("【Vision】本轮对话开销：" + str(prompt_tokens + completion_tokens) + "tokens，" + str(
                (prompt_tokens + completion_tokens) / 1000000 * 12) + "元")

            # 返回Kimi的回复

            return completion.choices[0].message.content

        except Exception as e:
            logger.error(e)
            return HandleError.handle_error(logger, e, role=role)  # 调用错误处理函数，返回错误类型







if __name__ == "__main__":
    client = OpenAI(
        api_key=AIConnect.read_api_key("/AISetting.json", logger=None, cache_choice=2),
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