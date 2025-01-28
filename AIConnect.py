from openai import OpenAI
from globals import global_state
import json
from ollama import Client


def AIConnector(logger, choice, temp=False):
    AI_Setting = parse_AI_Setting_json(logger, choice)
    if not AI_Setting:
        print("【AIConnector】读取API文件时发生错误")
        logger.error("【AIConnector】读取API文件时发生错误")
        return 0

    api_key = AI_Setting["api"]
    base_url = AI_Setting["url"]
    if not temp:
        global_state.G_model = AI_Setting["model"]
    else:
        print("【AIConnector】注意此次AI连接为临时！")
        logger.info("【AIConnector】注意此次AI连接为临时！")

    if choice > 1000:
        logger.info("【AIConnector】识别到本地模型请求，启动相关进程")
        client = Client(host='127.0.0.1:11434')
        logger.info("成功连接Model：" + str(AI_Setting["model"]) + "API名称：" + str(AI_Setting["api_name"]))
        return client

    else:
        logger.info("【AIConnector】识别到官方模型请求，启动相关进程")
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        logger.info("成功连接Model：" + str(AI_Setting["model"]) + "API名称：" + str(AI_Setting["api_name"]))
        logger.info("初始化计费器。当前消费：" + str(global_state.G_Consumption))
        return client



def parse_AI_Setting_json(logger, choice):
    """
    解析给定的JSON数据。

    参数:
    json_data (str): JSON格式的字符串。

    返回:
    list: 包含解析后的数据的列表。
    """
    try:
        with open("AISetting.json", 'r', encoding='utf-8') as file:
            # 使用json.load来读取文件内容并转换为字典
            json_data = json.load(file)
            for i in json_data:
                if i["code"] == choice:
                    logger.info("【parse_AI_Setting_json】找到了AI文件码：" + str(choice))
                    return i
    except FileNotFoundError:
        print(f"【parse_AI_Setting_json】文件AISetting.json未找到。")
        return 0
    except json.JSONDecodeError:
        print(f"【parse_AI_Setting_json】文件AISetting.json不是有效的JSON格式。")
        return 0
    except Exception as e:
        print(e)

        return 0

