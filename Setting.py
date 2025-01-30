import json
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod  # 导入抽象基类模块
# 第一组代码中的load_json_data函数
def load_json_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return (
            data['groups'],
            data['names'],
            data['admin_list'],
            data['VIP_list'],
            data['black_list']
        )
    except Exception as e:
        messagebox.showerror("错误", f"加载文件 {filename} 时出错：{e}")
        return None, None, None, None, None

# 第一组代码中的CheckboxManager和ExclusiveCheckboxManager类
class CheckboxManager:
    def __init__(self, master, names, initial_selections):
        self.names = names
        self.vars = {}
        self.btns = {}

        self.canvas = tk.Canvas(master, width=200, height=200)
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        for name in names:
            var = tk.BooleanVar(value=name in initial_selections)
            self.vars[name] = var
            btn = ttk.Checkbutton(
                self.frame, text=name, variable=var,
                command=lambda n=name: self.on_check(n)
            )
            btn.pack(anchor=tk.W)
            self.btns[name] = btn

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def on_check(self, name):
        pass

class ExclusiveCheckboxManager(CheckboxManager):
    def __init__(self, master, names, initial_selections, other_managers):
        super().__init__(master, names, initial_selections)
        self.other_managers = other_managers

        for name in names:
            if self.vars[name].get():
                self.disable_others(name)

    def disable_others(self, name):
        for manager in self.other_managers:
            manager.btns[name].config(state=tk.DISABLED)
            manager.vars[name].set(False)

    def enable_others(self, name):
        if not any(m.vars[name].get() for m in [self] + self.other_managers):
            for manager in self.other_managers:
                manager.btns[name].config(state=tk.NORMAL)

    def on_check(self, name):
        if self.vars[name].get():
            self.disable_others(name)
        else:
            self.enable_others(name)

# 第二组代码中的Setting类
class Setting:
    def __init__(self, file_path, role_file_path):
        self.settings = self.load_json(file_path)
        self.roles = self.load_json(role_file_path)
        self.code = None
        self.role_code = None
        self.is_suspended = False

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("错误", f"加载文件 {file_path} 时出错：{e}")
            return None

# 整合后的主窗口
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("综合设置管理")
        self.root.geometry("1200x600")  # 调整窗口大小以适应四个部分

        # 创建四个并列的LabelFrame
        self.admin_frame = ttk.LabelFrame(self.root, text="管理员名单", width=250, height=400)
        self.admin_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.vip_frame = ttk.LabelFrame(self.root, text="VIP名单", width=250, height=400)
        self.vip_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.black_frame = ttk.LabelFrame(self.root, text="黑名单", width=250, height=400)
        self.black_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.setting_frame = ttk.LabelFrame(self.root, text="设置", width=350, height=400)
        self.setting_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # 加载名单管理数据
        self.groups, self.names, self.admin_list, self.vip_list, self.black_list = load_json_data("lists.json")

        # 创建名单管理的复选框
        self.admin_mgr = ExclusiveCheckboxManager(self.admin_frame, self.names, self.admin_list, [])
        self.vip_mgr = ExclusiveCheckboxManager(self.vip_frame, self.names, self.vip_list, [self.admin_mgr])
        self.black_mgr = ExclusiveCheckboxManager(self.black_frame, self.names, self.black_list, [self.admin_mgr, self.vip_mgr])
        self.admin_mgr.other_managers = [self.vip_mgr, self.black_mgr]
        self.vip_mgr.other_managers = [self.admin_mgr, self.black_mgr]
        self.black_mgr.other_managers = [self.admin_mgr, self.vip_mgr]

        # 创建设置部分的控件
        self.setting = Setting("AISetting.json", "Role_and_Context/roles.json")
        self.create_setting_widgets()

        # 提交按钮
        self.submit_button = tk.Button(self.root, text="提交", command=self.on_submit)
        self.submit_button.grid(row=1, column=0, columnspan=4, pady=10)

    def create_setting_widgets(self):
        # 创建第一组下拉列表（URL）
        urls = list(set(item['url'] for item in self.setting.settings))
        self.url_combobox = ttk.Combobox(self.setting_frame, values=urls, width=40)
        self.url_combobox.grid(column=0, row=0, padx=10, pady=10)
        self.url_combobox.current(0)
        self.url_combobox.bind("<<ComboboxSelected>>", self.on_url_changed)

        # 创建第二组下拉列表（Model）
        self.model_combobox = ttk.Combobox(self.setting_frame, width=40)
        self.model_combobox.grid(column=0, row=1, padx=10, pady=10)
        self.model_combobox.bind("<<ComboboxSelected>>", self.on_model_changed)

        # 创建第三组下拉列表（API Name）
        self.api_name_combobox = ttk.Combobox(self.setting_frame, width=40)
        self.api_name_combobox.grid(column=0, row=2, padx=10, pady=10)

        # 创建第四组下拉列表（Role Name）
        role_names = [role['role_name'] for role in self.setting.roles]
        self.role_combobox = ttk.Combobox(self.setting_frame, values=role_names)
        self.role_combobox.grid(column=0, row=3, padx=10, pady=10)
        self.role_combobox.current(0)

        # 创建“挂起”复选框
        self.suspended_var = tk.BooleanVar()
        self.suspended_checkbox = tk.Checkbutton(self.setting_frame, text="挂起", variable=self.suspended_var)
        self.suspended_checkbox.grid(column=0, row=4, padx=10, pady=10)

    def on_url_changed(self, event):
        selected_url = self.url_combobox.get()
        models = [item['model'] for item in self.setting.settings if item['url'] == selected_url]
        if models:
            self.model_combobox['values'] = models
            self.model_combobox.current(0)
        else:
            messagebox.showwarning("警告", "所选URL无可用模型")

    def on_model_changed(self, event):
        selected_url = self.url_combobox.get()
        selected_model = self.model_combobox.get()
        api_names = [item['api_name'] for item in self.setting.settings if item['url'] == selected_url and item['model'] == selected_model]
        self.api_name_combobox['values'] = api_names
        self.api_name_combobox.current(0)

    def on_submit(self):
        # 收集名单管理部分的数据
        result = {
            'admin_list': [n for n in self.names if self.admin_mgr.vars[n].get()],
            'VIP_list': [n for n in self.names if self.vip_mgr.vars[n].get()],
            'black_list': [n for n in self.names if self.black_mgr.vars[n].get()],
            'groups': self.groups
        }

        # 收集设置部分的数据
        selected_url = self.url_combobox.get()
        selected_model = self.model_combobox.get()
        selected_api_name = self.api_name_combobox.get()
        selected_role_name = self.role_combobox.get()

        # 查找对应的code和role_code
        for item in self.setting.settings:
            if item['url'] == selected_url and item['model'] == selected_model and item[
                'api_name'] == selected_api_name:
                self.setting.code = item['code']
                break
        for role in self.setting.roles:
            if role['role_name'] == selected_role_name:
                self.setting.role_code = role['role_code']
                break
        self.setting.is_suspended = self.suspended_var.get()

        # 在销毁窗口之前，将结果存储到一个变量中
        self.result = {
            "名单管理": result,
            "设置": {
                "code": self.setting.code,
                "role_code": self.setting.role_code,
                "is_suspended": self.setting.is_suspended
            }
        }

        # 关闭窗口
        self.root.destroy()

        # 返回数据
        return {
            "名单管理": result,
            "设置": {
                "code": self.setting.code,
                "role_code": self.setting.role_code,
                "is_suspended": self.setting.is_suspended
            }
        }

# 定义一个抽象基类，用于定义接口
class ISettingManager(ABC):
    @abstractmethod
    def get_settings(self) -> dict:
        pass

# 实现抽象基类
class SettingManager(ISettingManager):
    def __init__(self, root):
        self.app = MainApp(root)
        self.result = None

    def get_settings(self) -> dict:
        self.result = self.app.on_submit()
        return self.result





def start_setting():
    while 1:
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()  # 启动主循环
        # 在窗口关闭后，从app中获取结果
        if hasattr(app, 'result'):
            settings = app.result
        else:
            print("【Setting】退出")
            exit(0)

        if not settings['名单管理']['admin_list']:
            print("【Setting】必须选择至少一个管理员，且Self必须包含在内！")
            continue
        if 'Self' not in settings['名单管理']['admin_list']:
            print("【Setting】必须选择Self为管理员！")
            continue
        if '文件传输助手' not in settings['名单管理']['groups']:
            print("【Setting】文件传输助手必须包含在监听列表中，请检查lists.json文件中的groups的值！")
            continue
        if not settings['设置']['code']:
            print("【Setting】AI选择无效！")
            continue

        print("————设置更新————")
        for i1, i2 in settings.items():
            print(i1)
            for j1, j2 in i2.items():
                print(f'{j1}: {j2}')
        print("——————————————")

        return settings

    # 使用示例
if __name__ == "__main__":
    start_setting()