import datetime
import Functions

from Functions import Reminder1_0 as Reminder_x

def function_console_command(logger, f_message, role = "New"):


    f_list = ["新功能"]
    f_code = 0
    f_instruction = ''
    f_who = ''
    f_time = datetime.datetime.now()
    # 解析f_message,解析出是那个功能、功能具体要求、是谁发起、在哪里发起、发起时间


    if f_code in f_list:
        if f_code == 1:
            return Reminder_x.reminder(logger,chat_to_who,)


    return 0;