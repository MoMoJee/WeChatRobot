import json

def read_dict_from_file(file_path = 'D:\\python_learn\\WeChatRobot\\Role_and_Context\\roles\\kimi-喵酱-初始版.json'):
    """
    从文件中读取字典。

    :param file_path: 文件路径
    :return: 读取的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用json.load来读取文件内容并转换为字典
            return json.load(file)
    except FileNotFoundError:
        print(f"【read_dict_from_file】文件 {file_path} 未找到。")
        return 0
    except json.JSONDecodeError:
        print(f"【read_dict_from_file】文件 {file_path} 不是有效的JSON格式。")
        return 0
    except:
        return 0

def return_role_words(logger, role_key, role_code):#为了加强拓展性和简化输入，这里用数码而非具体参数名称来实现返回项选择
    # role_sentence_dict是通过lrf函数读取的，键是句子代码，值是句子
    # role_key是句子代码，匹配并返回句子
    #  role_code是role文件的代码，将被解析成一个文件路径并导入lrf函数

    try:
        with open("Role_and_Context/roles.json", 'r', encoding='utf-8') as file:
            # 使用json.load来读取文件内容并转换为字典
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"【return_role_words】文件roles.json未找到。")
        return "0"
    except json.JSONDecodeError:
        print(f"【return_role_words】文件roles.json不是有效的JSON格式。")
        return "0"
    except Exception as e:
        print(e)

        return None



    role_file_path = json_data[role_code]["role_path"]

    if logger:
        logger.info("【return_role_words】已读取到role请求，role-key=" + role_key + ", role-code=" + str(role_code))
    role_sentence_dict = read_dict_from_file(file_path=role_file_path)

    if role_sentence_dict:
        return role_sentence_dict[role_key]
    else:
        logger.error("【return_role_words】人格文件的JSON格式出错或为空")
        return 'cache'






def write_dict_to_file(file_path, data_dict):
    """
    将字典写入到文件中。

    :param file_path: 文件路径
    :param data_dict: 要写入的字典
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 使用json.dump将字典写入文件
            json.dump(data_dict, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"写入文件时发生错误：{e}")











