import json
import tkinter as tk
from tkinter import ttk, messagebox



class Start_Setting:
    def __init__(self, file_path, role_file_path):
        self.settings = self.load_json(file_path)
        self.roles = self.load_json(role_file_path)
        self.code = None  # 初始化api_key为None
        self.role_code = None  # 初始化角色代码为None
        self.root = tk.Tk()
        self.root.title("设置")
        self.create_widgets()

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("错误", f"文件 {file_path} 未找到。")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("错误", f"文件 {file_path} 不是有效的JSON格式。")
            return None
        except Exception as e:
            messagebox.showerror("错误", str(e))
            return None

    def create_widgets(self):
        # 创建第一组下拉列表（URL）
        urls = list(set(item['url'] for item in self.settings))
        self.url_combobox = ttk.Combobox(self.root, values=urls, width=40)
        self.url_combobox.grid(column=0, row=0, padx=10, pady=10)
        self.url_combobox.current(0)  # 设置默认选项
        self.url_combobox.bind("<<ComboboxSelected>>", self.on_url_changed)

        # 创建第二组下拉列表（Model）
        self.model_combobox = ttk.Combobox(self.root, width=40)
        self.model_combobox.grid(column=0, row=1, padx=10, pady=10)
        self.model_combobox.bind("<<ComboboxSelected>>", self.on_model_changed)

        # 创建第三组下拉列表（API Name）
        self.api_name_combobox = ttk.Combobox(self.root, width=40)
        self.api_name_combobox.grid(column=0, row=2, padx=10, pady=10)

        # 创建第四组下拉列表（Role Name）
        role_names = [role['role_name'] for role in self.roles]
        self.role_combobox = ttk.Combobox(self.root, values=role_names)
        self.role_combobox.grid(column=1, row=0, padx=10, pady=10)
        self.role_combobox.current(0)  # 设置默认选项

        # 创建确认按钮
        self.confirm_button = tk.Button(self.root, text="确定", command=self.on_confirm)
        self.confirm_button.grid(column=0, row=4, padx=10, pady=10)

    def on_url_changed(self, event):
        selected_url = self.url_combobox.get()
        models = [item['model'] for item in self.settings if item['url'] == selected_url]
        self.model_combobox['values'] = models
        self.model_combobox.current(0)  # 设置默认选项

    def on_model_changed(self, event):
        selected_url = self.url_combobox.get()
        selected_model = self.model_combobox.get()
        api_names = [item['api_name'] for item in self.settings if item['url'] == selected_url and item['model'] == selected_model]
        self.api_name_combobox['values'] = api_names
        self.api_name_combobox.current(0)  # 设置默认选项

    def on_confirm(self):
        selected_url = self.url_combobox.get()
        selected_model = self.model_combobox.get()
        selected_api_name = self.api_name_combobox.get()
        selected_role_name = self.role_combobox.get()
        for item in self.settings:
            if item['url'] == selected_url and item['model'] == selected_model and item['api_name'] == selected_api_name:
                self.code = item['code']  # 存储api_key对应的code
                break
        for role in self.roles:
            if role['role_name'] == selected_role_name:
                self.role_code = role['role_code']  # 存储角色代码
                break
        messagebox.showinfo("结果", f"选中的API Key是: {self.code}\n选中的角色代码是: {self.role_code}")
        self.root.destroy()  # 关闭窗口

    def get_api_key_and_role_code(self):
        self.root.mainloop()  # 启动主循环
        return self.code, self.role_code  # 返回最终的api code和角色代码

def start_setting():
    api_file_path = "AISetting.json"
    role_file_path = "Role_and_Context/roles.json"
    selector = Start_Setting(api_file_path, role_file_path)
    code, role_code = selector.get_api_key_and_role_code()  # 获取最终的API Code和角色代码
    print(f"最终选中的AI Code是: {code}")
    print(f"最终选中的角色代码是: {role_code}")
    return {"model_code": code, "role_code": role_code}