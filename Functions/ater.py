import time
import datetime
from wxauto import WeChat

#微信接入
wx = WeChat()
# 首先设置一个监听列表，列表元素为指定好友（或群聊）的昵称
listen_list = ["五号楼花果山"]
# 然后调用`AddListenChat`方法添加监听对象，其中可选参数`savepic`为是否保存新消息图片
for i in listen_list:
    wx.AddListenChat(who=i)

#无限循环
while 1:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        one_msgs = msgs.get(chat)  # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            if msg.type == 'friend':
                sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名
                print("所有消息：",f'{sender.rjust(20)}：{msg.content}')
                if '@庞罗泽姻世伯' in msg.content:
                    chat.SendMsg('饱饱你是一个饱饱',at=msg.sender)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # 获取当前时间并打印
    time.sleep(1)
