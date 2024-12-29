# globals.py
class GlobalState:
    def __init__(self):
        self.conversation_History = {}
        self.Comsumption = 0
        self.model = ''
        self.Suspend = False
        self.global_log_file_path = "None"# 我真的只是因为懒才用这个的，尽量少用
        self.global_wx = "None"

# 创建单例实例
global_state = GlobalState()