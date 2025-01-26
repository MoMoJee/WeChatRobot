import random
from Role_and_Context import Role
def generate_exit_message(logger, role = 0):
    logger.info("【generate_cute_exit_message】随机结束语函数启动")
    # 这里可以定义一些可爱的退出语句，随机或按顺序选择
    exit_messages = Role.return_role_words(logger, role_key="1001", role_code=role)
    # 随机选择一条退出语句
    cute_exit_message = random.choice(exit_messages)
    logger.info('【generate_cute_exit_message】选择了退出提示：' + cute_exit_message)
    return cute_exit_message

def shutdown(logger):
    shutdown_password = random.getrandbits(100)
    logger.info("【shutdown】已生成本轮监听的强制终止密钥：" + str(shutdown_password))
    print("【shutdown】已生成本轮监听的强制终止密钥：" + str(shutdown_password))
    return shutdown_password
