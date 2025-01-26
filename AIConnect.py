from openai import OpenAI
from openai import RateLimitError  # 导入RateLimitError异常
import ollama
from ollama import Client
import globals
from globals import global_state


def AIConnector(logger, cache_choice=0):

    api_key = read_api_key('api_keys.txt', logger, cache_choice=cache_choice)
    if not api_key:
        print("读取API文件时发生错误")
        logger.error("【AIConnector】读取API文件时发生错误")
        return 0
    base_url = "https://api.moonshot.cn/v1"
    # base_url = "https://api.deepseek.com"
    global_state.model = "moonshot-v1-8k"
    # global_state.model = "deepseek-chat"
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



def read_api_key(file_path, logger, cache_choice = 0):
    """
    从指定的txt文件中读取API密钥，并根据用户选择的模型返回对应的API密钥

    参数:
    file_path (str): txt文件的路径

    返回:
    str: 用户选择的模型对应的API密钥
    """
    try:
        # 打开文件，使用只读模式
        with open(file_path, 'r') as file:
            # 读取文件内容并拆分为多行
            lines = file.readlines()

            # 用于存储模型和对应的API密钥
            api_keys = {}

            # 解析文件内容
            current_model = None
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    # 如果是以#开头的行，认为是模型名称
                    current_model = line[1:]  # 去掉#号
                    logger.info("【read_api_key】找到API：" + current_model)
                elif line:
                    # 如果不是空行，认为是API密钥
                    if current_model:
                        api_keys[current_model] = line
                        current_model = None  # 重置当前模型

            # 如果没有找到任何API密钥
            if not api_keys:
                logger.error("【read_api_key】文件中未找到有效的API密钥")
                print("【read_api_key】文件中未找到有效的API密钥")
                return None


            # 如果默认模型不为零，这代表函数在被调用前已经指定了密钥
            if cache_choice:
                try:
                    if 1 <= cache_choice <= len(api_keys):
                        selected_model = list(api_keys.keys())[cache_choice - 1]
                        logger.info(f"【read_api_key】指定了密钥：{list(api_keys.items())[cache_choice - 1]}：{api_keys[selected_model]}")
                        return api_keys[selected_model]
                    else:
                        print("【read_api_key】指定的编号无效，请重新输入。")
                        logger.error("【read_api_key】指定的编号无效")
                except ValueError:
                    print("【read_api_key】请指定有效的数字。")
                    logger.error("【read_api_key】指定无效。")


            # 显示可用的模型列表
            print("【read_api_key】可用的模型列表：")
            for i, model in enumerate(api_keys.keys(), 1):
                print(f"{i}. {model}")


            # 询问用户选择
            while True:
                try:
                    choice = int(input("【read_api_key】请选择要使用的模型（输入对应的编号）："))
                    if 1 <= choice <= len(api_keys):
                        selected_model = list(api_keys.keys())[choice - 1]
                        logger.info(f"【read_api_key】选择了密钥：{list(api_keys.items())[choice - 1]}：{api_keys[selected_model]}")
                        return api_keys[selected_model]
                    else:
                        print("【read_api_key】输入的编号无效，请重新输入。")
                        logger.error("【read_api_key】输入的编号无效")
                except ValueError:
                    print("【read_api_key】请输入有效的数字。")
                    logger.error("【read_api_key】输入无效。")

    except FileNotFoundError:
        print(f"【read_api_key】文件 {file_path} 未找到")
        logger.error(f"【read_api_key】文件 {file_path} 未找到")
        return None
    except Exception as e:
        print(f"【read_api_key】读取文件时发生错误：{e}")
        logger.error(f"【read_api_key】读取文件时发生错误：{e}")
        return None


# 示例用法

if __name__ == "__main__":
    file_path = 'api_keys.txt'  # 假设API密钥存储在当前目录下的api_key.txt文件中
    api_key = read_api_key(file_path)
    if api_key:
        print(f"读取到的API密钥为：{api_key}")