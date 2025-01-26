# WeChatRobot

项目起因是有人在微信群里说QQ有机器人微信为啥没有，然后就做了个赛博猫娘

期间群友偶尔会爆点金币，就磨磨唧唧做到了现在

这个文档包含部署方式和代码结构

## 1. 环境配置

### 1.1 python环境

其实只用了wxauto一个需要pip的，直接

```bash
pip install wxauto
```

我还引入了openai和ollama，用于链接部署在本地的AI模型（在AIConnect.py中），但说实话我并没有开始用这个，直接删掉这个import也行

```bash
pip install ollama
pip install openai
```



### 1.2 AI的API调用

在根目录下创建一个名为api_keys.txt的文件，格式大致为：

```
#kimi-WeChatRobot_moonshot-v1-8k
sk-123abcde33442

#deepseek-WeChatRobot_deepseek-chat
sk-fgg33-oo223440


即

#名称
api
```

两个连在一起即可，不同API之间空几行这个随意

然后在AIConnect.py的read_api_key函数会读取并让你选择API，这个功能是为了匹配选择模型的功能，<mark>不过我还没弄好，现在的choose_models函数还用不了</mark>

在API被读取之后，AI会连接



### 1.3 微信

微信登录即可。版本暂时没啥要求



## 2. 快速启动！

这个程序是支持自定义人格的，具体实现在Role_and_Context文件夹下

包含各类提示词、对话初始设定（即你给AI的人格）等

但是完整的人格替换我还没做完，很多还是硬编码的，尤其在Chatting、HandleError和ConsoleCommand中，改起来费劲

不过接口大多数我保留了，即大多数函数都有role参数，用来调用Role.py中的函数

因此暂时可以别管这个自定义



### 2.1 运行前的代码设置

#### 2.1.1 设置Main.py

##### 2.1.1.1 监听列表和人格码

在运行之前，设定listen_list和role_code（即人格文件，但我之前说了，这个还没写好，所以不要动这个0

"文件传输助手"是必须监听的，因为在运行过程中，由于主人和机器人公用一个账号

```python
listen_list = ["五号楼花果山", "文件传输助手"]
role_code = 0
```

##### 2.1.1.2  挂起状态



#### 2.1.2 设置responders.py

```python
blacklist = ['我是小天才']# 黑名单用户
adminlist = ['Self', '罗睿哲']# 管理员列表，！！！把Self作为管理员是方便从文件传输助手发送指令，Main函数中已经设定只接受和处理”文件传输助手“中的Self发送者，千万不能泄露，否则AI会自己给自己发指令
VIP_list = []
```

这里写昵称，注意：

对于有备注名的，设定为备注名

否则设定为其本人昵称，<mark>不是群昵称！</mark>