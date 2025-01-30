from wxauto import WeChat


def WeChatConnector(logger, listen_list):
    #微信接入
    try:
        wx = WeChat()
        logger.info("【WeChatConnector】微信接入成功")
        # 然后调用`AddListenChat`方法添加监听对象，其中可选参数`savepic`为是否保存新消息图片
        for i in listen_list:
            wx.AddListenChat(who=i, savepic=True)
            logger.info("【WeChatConnector】启用监听对象：" + str(i))

        return wx
    except Exception as e:
        error_str = str(e)
        logger.error("【WeChatConnector】未检测到微信登陆状态或未检测到监听窗口" + error_str)
        print("【WeChatConnector】未检测到登录窗口，请检查" + error_str)
        return 0

