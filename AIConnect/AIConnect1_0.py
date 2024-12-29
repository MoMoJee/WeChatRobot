from openai import OpenAI
from openai import RateLimitError  # 导入RateLimitError异常
import ollama
from ollama import Client
import globals
from  globals import global_state


def AIConnector(logger):

    api_key = "sk-m8SUBSaNEAwYWuEnqhL4loUTd6v96EPAUBVuNXT5eKnVzZYL"
    base_url = "https://api.moonshot.cn/v1"
    global_state.model = "moonshot-v1-8k"
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    logger.info("成功连接：apiKey=" + str(api_key) + "；Model：" + str(global_state.model))
    global_state.Comsumption = 0
    logger.info("初始化计费器。当前消费：" + str(global_state.Comsumption))
    return client

def choose_models(logger,message):
    # 假设这是大模型名称列表

    large_models = [
        "kimi",
        "glm4:9b-chat-q8_0",
        "glm4:9b-text-q8_0",
        "glm4:latest",
        "yi:9b",
        "phi3:14b",
        "llama3.2:3b",
        "qwen2.5:7b",
        "qwen2.5:14b",
        "qwen2.5:32b"
    ]
    print("可用的大模型列表：")
    logger.info("可用的大模型列表：")
    wx.SendMsg("请选择以下支持的模型：" + "\n ".join(large_models), who="文件传输助手") #这里不适用chat.SendMsg方法，是为了不传入chat这一复杂对象
    for model in large_models:
        print(model)
        logger.info(model)
    # 检查用户输入的模型名称是否在列表中
    find = 0 #创建布尔值确定是否成功查找
    for model in large_models:
        if model in message:
            logger.info("查找到指定的模型：" + model)
            print("查找到指定的模型：" + model)
            find = 1 #不对 这是冗余的。因为如果查找到了，循环会立即退出
            return model
    print("未查找到指定的模型：" + model)
    logger.error("未查找到指定的模型：" + model)
    wx.SendMsg("不支持的模型。请重新选择以下支持的模型：" + "\n".join(large_models), who="文件传输助手")
    return 0
# 这个晚点再写