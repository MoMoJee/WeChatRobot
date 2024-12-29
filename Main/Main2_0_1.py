import time
import datetime
from wxauto import WeChat
from openai import OpenAI
from openai import RateLimitError  # 导入RateLimitError异常
import os
import random
import json
import logging
import tkinter as tk
from tkinter import filedialog
import requests
import ollama
from ollama import Client

import Logger
from Logger import logger1_0 as logger_X
import ConsoleCommands
from ConsoleCommands import Console_Command1_0 as Console_Command_X
import Role_and_Context
from Role_and_Context import role1_0 as role_X
import History
from History import History1_0 as History_X
import Responders
from Responders import responders1_1 as responders_X
import Start_Close
from Start_Close import Start_Close1_0 as Start_Close_X
import AIConnect
from AIConnect import AIConnect1_0 as AIConnect_X
import globals
from  globals import global_state
import WeChatConnect
from WeChatConnect import WeChatConnector1_0 as WeChatConnector_X
import Functions
from Functions import function_console_command1_0 as function_console_command_X
from Functions import Reminder1_0 as Reminder_X

'''
2.0.1小优化：
1.增加程序关闭的方式，使得任意管理员都可以关闭，而非只能从主机的文件传输助手
2.增加main函数对role函数的支持
3.增加了消息获取检查，防止中途被迫下线而导致的中途停摆√
4.增加了对function的支持，使得聊天途中可以通过#fcc关键字启动function控制台
'''

listen_list = ["五号楼花果山","文件传输助手"]

logger = logger_X.start_logging("日志器", "日志")

global_state.conversation_History = History_X.Start_History(logger)
global_state.model = 'kimi'
global_state.Comsumption = 1

client = AIConnect_X.AIConnector(logger)




#开始监听
OutBreak=0#创建终止关键字
First = 1
global_state.Suspend = 0
connect_retry_times = 0

while 1:
    if OutBreak:
        break

    try:# 连接错误的处理，后期考虑放到HE函数那边
        msgs = wx.GetListenMessage()
    except:
        logger.error("【ConsoleCommand】未检测到微信登陆状态或未检测到监听窗口")
        print("【ConsoleCommand】未检测到微信登陆状态或未检测到监听窗口")
        wx = WeChatConnector_X.WeChatConnector(logger,listen_list)
        if wx:
            print("【ConsoleCommand】重连成功")
            logger.info("【ConsoleCommand】重连成功")
            global_state.global_wx = wx
            logger.info("【ConsoleCommand】全局变量global_state.global_wx已更新")
            shutdown_password = str(Start_Close_X.shutdown(logger))
            wx.SendMsg(msg=("已生成本轮监听的强制终止密钥：" + str(shutdown_password)), who="文件传输助手")
        else:
            print("【ConsoleCommand】重连失败")
            logger.error("【ConsoleCommand】重连失败")
            History_X.save_conversation_history_to_file(logger,global_state.conversation_History)
            print("【ConsoleCommand】已紧急写入历史记录到文件，可以强制关机")
            logger.warning("【ConsoleCommand】已紧急写入历史记录到文件，可以强制关机")
            connect_retry_times+=1
            time.sleep(60)
            if connect_retry_times >=100:
                OutBreak = 1
                logger.warning("【ConsoleCommand】已经超过10分钟没有连接成功，即将自动关机")
                print("【ConsoleCommand】已经超过10分钟没有连接成功，即将自动关机")
                break
        continue

    for chat in msgs:

        if OutBreak:
            break
        if First:
            chat.SendMsg('AI喵酱机器人启动！注意以下所有的【喵酱】发言都源自AI大模型，不代表本人观点，请谨慎识别喵！')
            logger.info('机器人启动词输出：AI喵酱机器人启动！注意以下所有的【喵酱】发言都源自AI大模型，不代表本人观点，请谨慎识别喵！')
            First = 0

        one_msgs = msgs.get(chat)  # 获取消息内容

        # 回复
        for msg in one_msgs:
            if shutdown_password in msg.content:
                print("【SuperCommand】收到强制关机密钥，程序已非正常停止运行")
                logger.warning("【SuperCommand】收到强制关机密钥，程序已非正常停止运行")
                History_X.save_conversation_history_to_file(logger,global_state.conversation_History)
                OutBreak = 1
            if OutBreak:
                break

            if global_state.Suspend:
                if "#cc" in f'{msg.content}' and '喵酱' in f'{msg.content}':# 挂起状态下，为了减轻计算负担，这里严格检验条件，只允许#cc指令运行，同时让AD鉴权，使得CC操作仍能进行
                    logger.info('接收到关键词' + f'{msg.sender}：{msg.content}')
                    chat.SendMsg(responders_X.Authenticator_Distributor(logger,msg,client))
                print("【ConsoleCommand】挂起中")
                continue

            #f = function_console_command_X.function_console_command(logger,msg)


            Reminder_X.reminder(l1,"五号楼花果山", {"目标0": ["未定义提醒0", "2024-12-29 20:16:02.189115"]})
            # 暂时还没想好这种实时监控的function和那种执行单词操作的function怎么分别处理
            # 在挂起状态下，应当只接受实时监控的function。
            # 反之则接收所以function，同时通过鉴权执行复杂function


            if msg.type == 'sys':
                logger.info('接收到新消息'+ f'【系统消息】{msg.content}')

            elif msg.type == 'friend':

                logger.info('接收到新消息' + f'【好友消息】{msg.sender}：{msg.content}')
             # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                if "喵酱" in f'{msg.content}':
                    logger.info('接收到关键词' + f'{msg.sender}：{msg.content}')
                    chat.SendMsg(responders_X.Authenticator_Distributor(logger,msg,client))

            elif msg.type == 'self':
                sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                print("所有消息：", f'{sender.rjust(20)}：{msg.content}')
                if chat.who == "文件传输助手":# 仅接收从文件传输助手接收到的#指令
                    # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                    if "喵酱@@退出" in f'{msg.content}':
                        logger.warning('【SuperCommand】请求：退出')
                        OutBreak = 1
                        print("退出")
                        chat.SendMsg(Start_Close_X.generate_cute_exit_message(logger))
                        # 保存对话历史到文件

                        History_X.save_conversation_history_to_file(logger, global_state.conversation_History)
                        logger.info("对话总消耗：" + str(global_state.Comsumption) + "tokens")
                        break
                    elif "#" in f'{msg.content}':
                        if "#sys" in f'{msg.content}' and '喵酱' in f'{msg.content}':
                            print("system请求")
                            logger.info('【system】请求：' + f'{msg.content}')
                            chat.SendMsg(responders_X.Authenticator_Distributor(logger, msg, client))

                        elif "#cc" in f'{msg.content}' and '喵酱' in f'{msg.content}':
                            print("Console请求")
                            logger.info('【Console】请求：' + f'{msg.content}')
                            chat.SendMsg("【喵酱Console Command】" + responders_X.Authenticator_Distributor(logger,msg,client))#跳转到鉴权，再跳转到控制台指令处理

                        else:
                            print("主人在控制台发起对话请求")#防止崩溃，我自己在文件传输助手里面聊天需要加一个#
                            if "喵酱" in f'{msg.content}':
                                logger.info('接收到主人新消息' + f'{sender}：{msg.content}')
                                chat.SendMsg(responders_X.Authenticator_Distributor(logger,msg,client))

                else:
                    if ("#cc" in f'{msg.content}') or ("喵酱@@退出" in f'{msg.content}') or ("#sys" in f'{msg.content}'):
                        logger.warning("接收到本机不来自控制台的控制台消息：" + f'{sender.rjust(20)}：{msg.content}')
                        print("接收到本机不来自控制台的控制台消息：" + f'{sender.rjust(20)}：{msg.content}')



            elif msg.type == 'time':
                print(f'\n【时间消息】{msg.time}')

            elif msg.type == 'recall':
                print(f'【撤回消息】{msg.content}')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 获取当前时间并打印
    time.sleep(0)

