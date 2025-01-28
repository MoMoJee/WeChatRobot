import Console_Command as Console_Command
import Chatting as Chatting
from globals import global_state
import History
from History import History as History
from Role_and_Context import Role as Role
from Functions import function_console_command

'''
1.1更新
1.优化AD函数处理逻辑
2.增设respond_VIPuser功能
3.VIP用户专用的function功能的引入
4.完善了对空消息回复的保护
5.增加了对role函数的支持
'''

def  Authenticator_Distributor(logger, msg, client, role = 0, special_0 = None):
    blacklist = ['我是小天才']
    adminlist = ['Self', '罗睿哲']# 管理员列表，！！！把Self作为管理员是方便从文件传输助手发送指令，Main函数中已经设定只接受和处理”文件传输助手“中的Self发送者，千万不能泄露，否则AI会自己给自己发指令
    VIP_list = []
    logger.info("【Authenticator_Distributor】启动鉴权进程")
    sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
    user_input = f'{sender}：{msg.content}'

    if sender in adminlist:# 管理员消息处理
        logger.info("【Authenticator_Distributor】接收到管理员消息")
        if "#cc" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【ConsoleCommand】指令：" + user_input)
            return Console_Command.Console_Command(logger, f'{msg.content}', '/History/Histories', client, role=role)
        elif "#sys" in f'{msg.content}':
            logger.info("【Authenticator_Distributor】接收到管理员【system】指令：" + user_input)
            return respond_sys(logger, user_input, client, role=role)
        else:
            logger.info("【Authenticator_Distributor】接收到管理员普通消息消息：" + user_input)
            return respond_VIPuser(logger, user_input, client, sender, role_code=role, fcc_need=special_0)

    elif sender in VIP_list:
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"

        else:
            logger.info("【Authenticator_Distributor】接收到VIP用户消息：" + user_input)
            return respond_VIPuser(logger, user_input, client,sender, role_code=role, fcc_need=special_0)

    elif sender in blacklist:
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"
        else:
            logger.info("【Authenticator_Distributor】接收到黑名单用户消息：" + user_input)
            return respond_bandeduser(logger, user_input, role=role)

    else:# 普通用户
        # 在挂起状态下所有人都可以用#cc走后门，这里补上这个漏洞
        if "#cc" in msg.content:
            logger.warning("【Authenticator_Distributor】接收到越权请求")
            return "【Authenticator_Distributor】没有#cc权限，请求被驳回"
        else:
            logger.info("【Authenticator_Distributor】接收到用户消息：" + user_input)
            return respond_user(logger, user_input, client, role_code=role)






def respond_user(logger, user_input, client, role_code = 0):
    AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'user', role=role_code)

    print(Role.return_role_words(logger, "0003", role_code) + f"说: {AI_reply}")
    role_key_word = Role.return_role_words(logger, "0001", role_code)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一条聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一组聊天记录")
        global_state.G_conversation_History = History.delete_n_messages(logger, global_state.G_conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一组历史记录")
        print("【respond_sys】已经安全删除上一组历史记录")
    return '【' + role_key_word + f'】{AI_reply}'

def respond_VIPuser(logger, user_input, client, sender, role_code = 0, fcc_need = None):
    role_key_word = Role.return_role_words(logger, "0001", role_code)
    # VIP用户增加function支持
    if "#f" in user_input:
        fcc_reply = function_console_command.function_console_command(logger, f'{user_input}', 1, f_special_1=sender, f_special_2=fcc_need, role=role_code)

        if fcc_reply['check']:
            # 向fcc发起请求，这里state状态为1。f_special_0用于传递client, f_special_1传递sender
            print("【respond_VIPuser】已执行function操作")
            AI_reply = fcc_reply['fs_return_0']
        else:
            logger.info("【respond_VIPuser】function操作执行失败")
            print('【respond_VIPuser】function操作执行失败')
            AI_reply = "f操作执行失败或未知的f指令"
    else:
        AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'user', role=role_code)
        print(Role.return_role_words(logger, "0003", role_code) + f"说: {AI_reply}")
        role_key_word = Role.return_role_words(logger, "0001", role_code)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一组聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一组聊天记录")
        global_state.G_conversation_History = History.delete_n_messages(logger, global_state.G_conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一组历史记录")
        print("【respond_sys】已经安全删除上一组历史记录")
    return '【' + role_key_word + f'】{AI_reply}'


def respond_sys(logger, user_input, client, role = 0):
    AI_reply = Chatting.chat_with_AI(logger, user_input, client, 'system', role=role)

    print(Role.return_role_words(logger, "0003", role) + f"说: {AI_reply}")
    role_key_word = Role.return_role_words(logger, "0001", role)
    if f'{AI_reply}' != "":
        logger.info('【大模型回复】【' + role_key_word + f'】{AI_reply}')
    else:
        logger.warning("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一组聊天记录")
        print("【respond_sys】一个尝试回复空消息的尝试被阻止，正在清除上一组聊天记录")
        global_state.G_conversation_History = History.delete_n_messages(logger, global_state.G_conversation_History, 1)
        logger.info("【respond_sys】已经安全删除上一组历史记录")
        print("【respond_sys】已经安全删除上一组历史记录")
    return '【' + role_key_word + f'】{AI_reply}'

def respond_bandeduser(logger, user_input, role = 0):

    return "【喵酱】不理你"

