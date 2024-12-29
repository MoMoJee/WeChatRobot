from wxauto import WeChat


def WeChatConnector(logger,listen_list):
    #微信接入
    try:
        wx = WeChat()
        logger.info("【WeChatConnector】微信接入成功")
        # 然后调用`AddListenChat`方法添加监听对象，其中可选参数`savepic`为是否保存新消息图片
        for i in listen_list:
            wx.AddListenChat(who=i)
            logger.info("【WeChatConnector】启用监听对象：" + str(i))
        return wx
    except:
        print("【WeChatConnector】未检测到登录窗口，请检查")
        logger.error("【WeChatConnector】未检测到登录窗口")
        return 0

