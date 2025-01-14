import ConsoleCommands
from ConsoleCommands import Console_Command1_0 as Console_Command
import Chatting
from Chatting import Chatting as Chatting
import globals
from  globals import global_state
import Functions
from Functions import function_console_command as function_console_command
import History
from History import History as History
import Role_and_Context
from Role_and_Context import Role as Role

'''
1.1更新
1.优化AD函数处理逻辑
2.增设respond_VIPuser功能
3.VIP用户专用的function功能的引入
4.完善了对空消息回复的保护
5.增加了对role函数的支持
'''

def  Authenticator_Distributor(logger, msg, client, role = 0):
    blacklist = ['我是小天才']
    adminlist = ['Self', '罗睿哲']# 管理员列表，！！！把Self作为管理员是方便从文件传输助手发送指令，Main函数中已经设定只接受和处理”文件传输助手“中的Self发送者，千万不能泄露，否则AI会自己给自己发指令
    VIP_list = []
    logger.info("【Authenticator_Distributor】启动鉴权进程")
    sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
    user_input = f'{sender.rjust(20)}：{msg.content}'

    if sender in adminlist:# 管理员消息处理
        logger.info("【Authenticator_Distributor】接收到管理员消息")
        if "#cc" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【ConsoleCommand】指令：" + user_input)
            return Console_Command.Console_Command(logger, f'{msg.content}', 'D:\\python_learn\\WeChatRobot\\History\\Histories', client, role=role)
        elif "#sys" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【system】指令：" + user_input)
            return respond_sys(logger, user_input, client, role=role)
        else:
            logger.info("【Authenticator_Distributor】接收到管理员普通消息消息：" + user_input)
            return respond_VIPuser(logger, user_input, client, role=role)

    elif sender in VIP_list:
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"
        else:
            logger.info("【Authenticator_Distributor】接收到VIP用户消息：" + user_input)
            return respond_VIPuser(logger, user_input, client, role=role)

    elif sender in blacklist:
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"
        else:
            logger.info("【Authenticator_Distributor】接收到黑名单用户消息：" + user_input)
            return respond_bandeduser(logger,user_input, role=role)

    else:# 普通用户
        # 在挂起状态下所有人都可以用#cc走后门，这里补上这个漏洞
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"
        else:
            logger.info("【Authenticator_Distributor】接收到用户消息：" + user_input)
            return respond_user(logger,  user_input, client, role=role)






def respond_user(logger, user_input, client, role = 0):
    AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'user')

    print(Role.return_role_words(logger, "0003", role) + f"说: {AI_reply}")
    role_key_word = Role.return_role_words(logger, "0001", role)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        global_state.conversation_History = History.delete_n_messages(logger, global_state.conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一条历史记录")
        print("【respond_sys】已经安全删除上一条历史记录")
    return '【' + role_key_word + f'】{AI_reply}'

def respond_VIPuser(logger, user_input, client, role = 0):

    #VIP用户增加function支持
    AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'user')
    print(Role.return_role_words(logger, "0003", role) + f"说: {AI_reply}")
    role_key_word = Role.return_role_words(logger, "0001", role)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        global_state.conversation_History = History.delete_n_messages(logger, global_state.conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一条历史记录")
        print("【respond_sys】已经安全删除上一条历史记录")
    return '【' + role_key_word + f'】{AI_reply}'


def respond_sys(logger, user_input, client, role = 0):
    AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'system')

    print(Role.return_role_words(logger, "0003", role) + f"说: {AI_reply}")
    role_key_word = Role.return_role_words(logger, "0001", role)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        global_state.conversation_History = History.delete_n_messages(logger, global_state.conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一条历史记录")
        print("【respond_sys】已经安全删除上一条历史记录")
    return '【' + role_key_word + f'】{AI_reply}'

def respond_bandeduser(logger, user_input, role = 0):

    return "【喵酱】不理你"

