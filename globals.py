# globals.py
class GlobalState:
    def __init__(self):
        self.G_conversation_History = {}
        self.G_Consumption = 0
        self.G_model = ''
        self.G_model_code = 0
        self.G_Suspend = False
        self.G_global_log_file_path = "None"# 我真的只是因为懒才用这个的，尽量少用
        self.G_wx = "None"

# 创建单例实例
global_state = GlobalState()