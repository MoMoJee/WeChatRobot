import datetime

from Functions import Reminder as Reminder
from Functions import Vision

# fcc有两种调用方式，一种是在Main中通过监控直接调用，用于需要实时监控在线的function
# 另一种是在接收到关键字后通过responder调用（包括鉴权）
# 这两种调用方式对应的function应该是不同的，为了防止（主要是）responder方式调用的输入错误地指向了本应由监控方式调用的，我设置state参数来区分不同的调用入口
# 因为fcc通过消息中的关键字来链接不同的function，而为了方便，监控调用fcc会直接在接口中键入关键字（虽然可以设置地很复杂但是（））
# 就比如有人在输入里启动了responder，输入里又有”创建提醒“，如果没有state检查，就会错误地开启本应自动按照时间启动的reminder，导致未知的错误（比如输入的参数reminder函数无法识别）

def function_console_command(logger, f_message, state=0, f_special_0=None, f_special_1=None, f_special_2=None, role="New"):
    #  好新颖的想法，通过指定未指定作用的形参，接收不同功能可能用到的不同变量
    f_dict = {0: "未定义功能", 1: "reminder", 2: "remind_setter", 3: "v"}
    # 各个功能的值不能有重复！
    f_code = 0
    f = "未定义功能"
    f_time = datetime.datetime.now()
    for f_code, f in f_dict.items():
        # 解析请求类型，返回请求代码
        if f in f_message:
            if state:
                # 简化日志，只有从ad发送的fcc请求才被日志记录，从监控台发出的则不被记录
                logger.info("【function_console_command】已读取到fcc请求：" + f + "请求代码：" + str(f_code))
            break
        else:
            f_code = 0
            f = "未定义功能"



    # 解析f_message,解析出是那个功能、功能具体要求、是谁发起、在哪里发起、发起时间
    # function 完全脱离main中的方法，而是在各个function函数中执行操作，
    # 因此FCC只返回0或1，表示main收到并转发的请求是否通过了FCC的检查
    # 不对啊 fcc的返回值形式是可以根据if来变的。emmmm再想想。
    # 灵活返回确实方便，但是容易搞混 不如整一个统一的接口协议
    f_message_dict = {'f_message': f_message, 'f': f, 'f_code': f_code, 'f_time': str(f_time)}

        #统一的return接口：
    check = 0# fcc检查结果
    fcc_message_dict = {}# 返回上面解析f_message的结果，可选吧，不一定要全部返回
    fcc_prompt = ""# 返回fcc的提示，比如鉴权失败，成功接入，缺少参数等等（如果配备了错误处理的话，尤其是比如，remind_setter，未解析到时间、对象、提醒词中任意一个）
    fcc_special_0 = None
    fs_return_0 = None
    fs_return_1 = None
    fs_return_2 = None
    fs_special_0 = None

    if f_code in f_dict:
        if f_code == 1:
            #
            if Reminder.reminder(logger, chat=f_special_0, role="New"):
                # f_special_0在reminder函数中用于传入chat对象
                check = 1
            else:
                check = 0
                logger.warning("【function_console_command】reminder检查不通过，可能出现了网络问题等")
                fcc_prompt = "【function_console_command】reminder检查不通过，可能出现了网络问题等"
        elif f_code == 3:
            # 0是client，1是sender，2是路径列表
            path = find_last_image_by_sender(logger, f_special_2, f_special_1)
            logger.info("【function_console_command】找到了最近的图片路径：" + str(path))
            # 根据sender，在列表中查找这个sender发的上一个图片，解析
            if path:
                vision_reply = Vision.vision(logger, user_message=f_message, client=f_special_0, user_role="user", image_path=path)
            else:
                vision_reply = "你发了个啥？"
                fcc_prompt = "未获取到用户的上一条图片信息"
            fs_return_0 = vision_reply
            check = 1




    return {
            'check' : check,
            'f_message_dict' : f_message_dict,
            'fcc_prompt' : fcc_prompt,
            'fcc_special_0' : fcc_special_0,
            'fs_return_0' : fs_return_0,
            'fs_return_1' : fs_return_1,
            'fs_return_2' : fs_return_2,
            'fs_special_0' : fs_special_0
            }# 超高带宽的返回，我觉着其他的大型控制函数，作为“集线器”，也可以参考这种做法



def find_last_image_by_sender(logger, image_list, target_sender):
    """
    在image_list中从后往前查找第一个键'sender'的值为target_sender的字典，并返回其'value'

    参数:
    image_list (list): 存储着多个sender: path的字典的列表
    target_sender (str): 要查找的目标sender

    返回:
    str: 找到的path值，如果没有找到则返回None
    """
    # 从后往前遍历列表
    try:
        for image_dict in reversed(image_list):
            # 如果找到匹配的sender，返回对应的path
            if image_dict["sender"] == target_sender:
                return image_dict["path"]
        # 如果遍历完列表都没有找到匹配的sender，返回None
    except Exception as e:
        return e
    return None

# 示例用法
if __name__ == "__main__":

    image_list = [
        {"sender": "user1", "path": "/path/to/image1"},
        {"sender": "user2", "path": "/path/to/image2"},
        {"sender": "user1", "path": "/path/to/image3"},
        {"sender": "user3", "path": "/path/to/image4"}
    ]

    target_sender = "user1"
    result_path = find_last_image_by_sender("1", image_list, target_sender)
    if result_path:
        print(f"找到的path为：{result_path}")
    else:
        print(f"未找到sender为{target_sender}的记录")