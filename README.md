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

### 2.1 运行需要的文件

#### 2.1.1 AISetting.json

之前讲了

#### 2.1.2 lists.json

```json
{
    "groups": ["文件传输助手", "五号楼花果山"],
    "names": ["Self", "我是小天才", "壹只卡皮巴拉"],
    "admin_list": ["Self"],
    "VIP_list": ["壹只卡皮巴拉"],
    "black_list": ["我是小天才"]
}
```

第一行是监听对象，文件传输助手一定要有，后者是你要监听的群，虽然你写多个不会报错，但建议只写一个，因为聊天记录是共享的

第二行是可选的聊天对象，先写进去，然后后三行才能写。相当于一个总名单，三个分名单。（后三行其实是默认值啦）

要写昵称，注意：

对于有备注名的，设定为备注名

否则设定为其本人昵称，<mark>不是群昵称！</mark>



#### 2.1.3 role文件

可以打开看看，给了示例的



#### 2.1.4 history文件

也给了示例，需要对应你选择的模型！当然你从0开始（Zero.txt）也行



### 2.2 启动！

运行Main.py，生成的设置界面，如果之前你做对了，那么一点问题没有

### 2.2 #cc指令