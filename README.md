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

我还引入了openai和ollama，用于链接部署在本地的AI模型（在AIConnect.py中）

```bash
pip install ollama
pip install openai
```

### 1.2 AI的API调用

在根目录下创建一个名为AISetting.json的文件，格式大致为：

注意替换为你自己的AI文件

```json
[
    {
        "url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "api": "xxx",
        "api_name": "WeChatRobot_deepseek-chat",
        "code": 1
    },
    {
        "url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "api": "xxx",
        "api_name": "WeChatRobot_moonshot-v1-8k",
        "code": 2
    },
    {
        "url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k-vision-preview",
        "api": "xxx",
        "api_name": "WeChatRobot_moonshot-v1-vision",
        "code": 3
    },
    {
        "url": "http://127.0.0.1:11434/",
        "model": "deepseek-r1:14b",
        "api": 0,
        "api_name": "deepseek-r1:14b_API",
        "code": 1001
    },
    {
        "url": "http://127.0.0.1:11434/",
        "model": "deepseek-r1:7b",
        "api": 0,
        "api_name": "deepseek-r1:7b_API",
        "code": 1002
    }
]
```

然后在AIConnect.py的函数会读取并让你选择API

在API被读取之后，AI会连接

### 1.3 微信

微信登录即可。版本暂时没啥要求

## 2. 快速启动！

这个程序是支持自定义人格的，具体实现在Role_and_Context文件夹下

包含各类提示词、对话初始设定（即你给AI的人格）等

### 2.1 运行前的代码设置

#### 2.1.1 设置Main.py

##### 2.1.1.1 监听列表和人格码

在运行之前，设定listen_list

"文件传输助手"是必须监听的，因为在运行过程中，由于主人和机器人公用一个账号，这相当于控制台

```python
listen_list = ["五号楼花果山", "文件传输助手"]
role_code = 0
```

##### 2.1.1.2  挂起状态

挂起状态下，机器人只会监听消息，回复#cc控制台消息。#cc指令集见下

```python
global_state.G_Suspend = 0# 挂起状态
```

#### 2.1.2 设置responders.py

```python
blacklist = ['我是小天才']# 黑名单用户
adminlist = ['Self', '罗睿哲']# 管理员列表，！！！把Self作为管理员是方便从文件传输助手发送指令，Main函数中已经设定只接受和处理”文件传输助手“中的Self发送者，千万不能泄露，否则AI会自己给自己发指令
VIP_list = []# VIP用户
```

这里写昵称，注意：

对于有备注名的，设定为备注名

否则设定为其本人昵称，<mark>不是群昵称！</mark>



### 2.2 #cc指令