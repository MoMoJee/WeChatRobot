import ConsoleCommands
from ConsoleCommands import Console_Command1_0 as Console_Command_X
import Chatting
from Chatting import Chatting as Chatting_X
import globals
from  globals import global_state

def  Authenticator_Distributor(logger, msg, client, role = "New"):
    blacklist = []
    adminlist = ['Self', '罗睿哲']# 管理员列表，！！！把Self作为管理员是方便从文件传输助手发送指令，Main函数中已经设定只接受和处理”文件传输助手“中的Self发送者，千万不能泄露，否则AI会自己给自己发指令
    VIP_list = []
    logger.info("【Authenticator_Distributor】启动鉴权进程")
    sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
    user_input = f'{sender.rjust(20)}：{msg.content}'

    if sender in adminlist:
        logger.info("【Authenticator_Distributor】接收到管理员消息")
        if "#cc" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【ConsoleCommand】指令：" + user_input)
            return Console_Command_X.Console_Command(logger, f'{msg.content}', 'D:\\python_learn\\WeChatRobot\\History\\Histories', client)
        elif "#sys" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【system】指令：" + user_input)
            return respond_sys(logger, user_input, client)
        else:
            logger.info("【Authenticator_Distributor】接收到管理员普通消息消息：" + user_input)
            return respond_user(logger, user_input, client)

    elif sender in VIP_list:
        ogger.info("【Authenticator_Distributor】接收到VIP用户消息：" + user_input)
        return respond_user(logger, f'{sender.rjust(20)}：{msg.content}', client)# 没想好VIP可以干嘛

    elif sender in blacklist:
        ogger.info("【Authenticator_Distributor】接收到黑名单用户消息：" + user_input)
        return respond_bandeduser(logger,user_input)

    else:# 普通用户
        ogger.info("【Authenticator_Distributor】接收到用户消息：" + user_input)
        return respond_user(logger, f'{sender.rjust(20)}：{msg.content}', client)



def respond_user(logger, user_input, client, role = "New"):
    AI_reply = Chatting_X.chat_with_AI(logger,user_input, client,'user')
    print(f"喵酱说: {AI_reply}")
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】' + f'【喵酱】{AI_reply}')
    else:
        chat.SendMsg("【喵酱】我不能发空白信息喵")
        logger.warning("一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        # 我还没写，这里是对历史记录中的上一条聊天记录执行抹去

        # 此处将msg.content传递给大模型，再由大模型返回的消息回复即可实现ai聊天
    return f'【喵酱】{AI_reply}'


def respond_sys(logger, user_input, client, role = "New"):
    AI_reply = Chatting_X.chat_with_AI(logger,user_input,client,"system")
    print(f"喵酱说: {AI_reply}")
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】' + f'【喵酱】{AI_reply}')
    else:
        chat.SendMsg("【喵酱】我不能发空白信息喵")
        logger.warning("一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        # 我还没写，这里是对历史记录中的上一条聊天记录执行抹去

        # 此处将msg.content传递给大模型，再由大模型返回的消息回复即可实现ai聊天
    return f'【喵酱】{AI_reply}'


def respond_bandeduser(logger, user_input, role = "New"):
    return "【喵酱】不理你"