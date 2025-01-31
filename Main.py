import time
import datetime
from Logger import Logger as Logger
from Role_and_Context import Role as Role
from History import History as History
import responders as responders
import Start_Close as Start_Close
import AIConnect as AIConnect
import Setting
from globals import global_state
import WeChatConnector as WeChatConnector
from Functions import function_console_command as function_console_command




start_setting = 404
while start_setting == 404:
    start_setting = Setting.start_setting()
    if not start_setting:
        exit(0)

listen_list = start_setting['名单管理']['groups']
admin_list = start_setting['名单管理']['admin_list']
black_list = start_setting['名单管理']['black_list']
VIP_list = start_setting['名单管理']['VIP_list']
role_code = start_setting['设置']['role_code']
choice = start_setting['设置']['code']
global_state.G_model_code = choice
global_state.G_Suspend = start_setting['设置']['is_suspended']# 挂起状态




logger = Logger.start_logging(log_name=Role.return_role_words(logger=0, role_key="0000", role_code=role_code))
# logger还没创建，So。。。
client = AIConnect.AIConnector(logger, choice=choice, temp=False)
# 这里设置要用哪个AI，choice是序号，写在AISetting.json里面



global_state.G_conversation_History = History.Start_History(logger)
global_state.G_Consumption = 1
image_list = []
# 这里存储接收到的图片的路径，格式是一系列字典存储在列表中，{sender: path}

# 开始监听
OutBreak = 0
# 创建终止关键字
First = 1

connect_retry_times = 0

role_keyword = Role.return_role_words(logger, role_key="0001", role_code=role_code)

while 1:
    if OutBreak:
        break
    if global_state.G_error_code:
        print(f"【ConsoleCommand】检测到主错误码：{global_state.G_error_code}")
        logger.error(f"【ConsoleCommand】检测到主错误码：{global_state.G_error_code}")
        if global_state.G_error_code == 1:
            client = AIConnect.AIConnector(logger, choice=global_state.G_model_code, temp=False)
            global_state.G_error_code = 0
            # 更多错误码处理逻辑
        elif global_state.G_error_code == 2:

            start_setting = 0
            while not start_setting:
                start_setting = Setting.start_setting()

            if start_setting != 404:
                admin_list = start_setting['名单管理']['admin_list']
                black_list = start_setting['名单管理']['black_list']
                VIP_list = start_setting['名单管理']['VIP_list']

                if start_setting['设置']['role_code'] != role_code:
                    print("【ConsoleCommand】运行中禁止修改role参数！设置被驳回")
                    logger.warning("【ConsoleCommand】运行中禁止修改role参数！设置被驳回")
                choice = start_setting['设置']['code']
                global_state.G_Suspend = start_setting['设置']['is_suspended']  # 挂起状态

                if listen_list != start_setting['名单管理']['groups']:
                    logger.info("【ConsoleCommand】检测到修改监听对象指令")
                    listen_list = start_setting['名单管理']['groups']
                    wx = WeChatConnector.WeChatConnector(logger, listen_list)

                if global_state.G_model_code != choice:
                    logger.info("【ConsoleCommand】模型码已修改为：" + str(choice))
                    global_state.G_model_code = choice
                    global_state.G_model = AIConnect.parse_AI_Setting_json(logger, choice)["model"]
                    logger.info("【ConsoleCommand】模型已修改为：" + global_state.G_model)
                    logger.info("【ConsoleCommand】重新连接模型")
                    client = AIConnect.AIConnector(logger, choice=choice, temp=False)
                    if client:
                        global_state.G_error_code = 0
                        logger.info(f"【ConsoleCommand】设置修改成功！当前设置：{str(start_setting)}")
                    else:
                        logger.error("【ConsoleCommand】模型连接出错，请重新设置")
                else:
                    global_state.G_error_code = 0
                    logger.info(f"【ConsoleCommand】设置修改成功！当前设置：{str(start_setting)}")

            else:
                global_state.G_error_code = 0
                logger.info("【ConsoleCommand】用户已取消设置")


    try:# 连接错误的处理，后期考虑放到HE函数那边
        msgs = wx.GetListenMessage()

    except Exception as e:
        error_str = str(e)
        logger.error("【ConsoleCommand】未检测到微信登陆状态或未检测到监听窗口" + error_str)
        print("【ConsoleCommand】未检测到微信登陆状态或未检测到监听窗口" + error_str)
        wx = WeChatConnector.WeChatConnector(logger, listen_list)
        if wx:
            print("【ConsoleCommand】重连成功")
            logger.info("【ConsoleCommand】重连成功")
            global_state.G_wx = wx
            logger.info("【ConsoleCommand】全局变量global_state.global_wx已更新")
            shutdown_password = str(Start_Close.shutdown(logger))
            wx.SendMsg(msg=("已生成本轮监听的强制终止密钥：" + str(shutdown_password)), who="文件传输助手")
        else:
            print("【ConsoleCommand】重连失败")
            logger.error("【ConsoleCommand】重连失败")
            History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role_code)
            print("【ConsoleCommand】已紧急写入历史记录到文件，可以强制关机")
            logger.warning("【ConsoleCommand】已紧急写入历史记录到文件，可以强制关机")
            connect_retry_times += 1
            time.sleep(20)
            if connect_retry_times >= 30:
                OutBreak = 1
                logger.warning("【ConsoleCommand】已经超过10分钟没有连接成功，即将自动关机")
                print("【ConsoleCommand】已经超过10分钟没有连接成功，即将自动关机")
                break
        continue

    for chat in msgs:

        if OutBreak:
            break
        if First:
            chat.SendMsg(Role.return_role_words(logger, "0002", role_code))
            logger.info('【SuperCommand】机器人启动词已输出')
            First = 0

        one_msgs = msgs.get(chat)  # 获取消息内容

        # 回复
        for msg in one_msgs:
            if shutdown_password in msg.content:
                print("【SuperCommand】收到强制关机密钥，程序已非正常停止运行")
                logger.warning("【SuperCommand】收到强制关机密钥，程序已非正常停止运行")
                History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role_code)
                OutBreak = 1
            if OutBreak:
                break


            """
            if function_console_command.function_console_command(logger, "reminder", 0, f_special_0=chat, role=role_code)['check']:
                # 向fcc发起reminder请求，这里state状态为0，因为是从监控台调用的。f_special_0用于传递chat
                print("【ConsoleCommand】已执行提醒操作")
            else:
                logger.info("【ConsoleCommand】提醒操作执行失败")
                print('【ConsoleCommand】提醒操作执行失败')
            """


            # 暂时还没想好这种实时监控的function和那种执行单词操作的function怎么分别处理
            # 在挂起状态下，应当只接受实时监控的function。
            # 反之则接收所以function，同时通过鉴权执行复杂function


            if global_state.G_Suspend:

                if "#cc" in f'{msg.content}' and role_keyword in f'{msg.content}':
                    # 挂起状态下，为了减轻计算负担，这里严格检验条件，只允许#cc指令运行，同时让AD鉴权，使得CC操作仍能进行
                    # 在非挂起状态下，来自self的#cc指令只能在文件传输助手中有效，在其他界面会提示：接收到本机不来自控制台的控制台消息
                    logger.info('接收到关键词' + f'{msg.sender}：{msg.content}')
                    chat.SendMsg(
                        responders.Authenticator_Distributor(logger, msg, client, role=role_code, black_list=black_list,
                                                             admin_list=admin_list, VIP_list=VIP_list))
                print("【ConsoleCommand】挂起中")
                continue




            if msg.type == 'sys':
                logger.info('【ConsoleCommand】接收到新消息'+ f'【系统消息】{msg.content}')

            elif msg.type == 'friend':
                logger.info('【ConsoleCommand】接收到新消息' + f'【好友消息】{msg.sender}：{msg.content}')

                if "WeChatRobot\wxauto文件" in msg.content:
                    image_list.append({"sender": msg.sender, "path": msg.content})
                    # 存储所有的图片路径

                # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                if role_keyword in f'{msg.content}':
                    logger.info('【ConsoleCommand】接收到关键词' + f'{msg.sender}：{msg.content}')
                    chat.SendMsg(
                        responders.Authenticator_Distributor(logger, msg, client, role=role_code, special_0=image_list, black_list=black_list,
                                                             admin_list=admin_list, VIP_list=VIP_list), at=msg.sender)

            elif msg.type == 'self':
                sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                print("【ConsoleCommand】接收到新消息" + f'【控制台消息】{sender}：{msg.content}')
                logger.info("【ConsoleCommand】接收到新消息" + f'【控制台消息】{sender}：{msg.content}')
                if chat.who == "文件传输助手":# 仅接收从文件传输助手接收到的#指令
                    if "WeChatRobot\wxauto文件" in msg.content:
                        image_list.append({"sender": msg.sender, "path": msg.content})
                        print(image_list)
                        # 存储所有的图片路径
                    # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                    if (role_keyword + "@@退出") in f'{msg.content}':
                        logger.warning('【SuperCommand】请求：退出')
                        OutBreak = 1
                        print("【SuperCommand】退出")
                        chat.SendMsg(Start_Close.generate_exit_message(logger, role=role_code))
                        # 保存对话历史到文件

                        History.save_conversation_history_to_file(logger, global_state.G_conversation_History, role=role_code)
                        logger.info("【SuperCommand】对话总消耗：" + str(global_state.G_Consumption) + "tokens")
                        break
                    elif "#" in f'{msg.content}':
                        if "#sys" in f'{msg.content}' and role_keyword in f'{msg.content}':
                            print("【ConsoleCommand】system请求")
                            logger.info('【ConsoleCommand】【system】请求：' + f'{msg.content}')
                            chat.SendMsg(responders.Authenticator_Distributor(logger, msg, client, role=role_code, black_list=black_list,
                                                             admin_list=admin_list, VIP_list=VIP_list))

                        elif "#cc" in f'{msg.content}' and role_keyword in f'{msg.content}':
                            print("【ConsoleCommand】【Console】请求")
                            logger.info('【ConsoleCommand】【Console】请求：' + f'{msg.content}')
                            chat.SendMsg("【Console Command】" + responders.Authenticator_Distributor(logger, msg, client,
                                                                                                    role=role_code,
                                                                                                    black_list=black_list,
                                                                                                    admin_list=admin_list,
                                                                                                    VIP_list=VIP_list))  # 跳转到鉴权，再跳转到控制台指令处理
                        else:
                            print("【ConsoleCommand】主人在控制台发起对话请求")# 防止崩溃，我自己在文件传输助手里面聊天需要加一个#
                            if role_keyword in f'{msg.content}':
                                logger.info('【ConsoleCommand】接收到主人新消息' + f'{sender}：{msg.content}')
                                chat.SendMsg(responders.Authenticator_Distributor(logger, msg, client, role=role_code,
                                                                                  special_0=image_list,
                                                                                  black_list=black_list,
                                                                                  admin_list=admin_list,
                                                                                  VIP_list=VIP_list
                                                                                  ))

                else:
                    if ("#cc" in f'{msg.content}') or ((role_keyword + "@@退出") in f'{msg.content}') or ("#sys" in f'{msg.content}'):
                        logger.warning("接收到本机不来自控制台的控制台消息：" + f'{sender.rjust(20)}：{msg.content}')
                        print("接收到本机不来自控制台的控制台消息：" + f'{sender.rjust(20)}：{msg.content}')



            elif msg.type == 'time':
                print(f'\n【时间消息】{msg.time}')

            elif msg.type == 'recall':
                print(f'【撤回消息】{msg.content}')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))# 获取当前时间并打印
    time.sleep(1)


