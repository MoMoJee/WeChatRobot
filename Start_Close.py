import random

def generate_cute_exit_message(logger, role = "New"):
    logger.info('随机结束语函数启动')
    # 这里可以定义一些可爱的退出语句，随机或按顺序选择
    exit_messages = [
        "呜~主人要离开喵酱了，我会想你的~记得下次再来找喵酱玩哦~",
        "喵~是时候说再见了，喵酱会在这里等你的~下次见喵~",
        "啊呜~主人要忙了吗？喵酱会乖乖的，期待和主人的下次相遇喵~",
        "喵喵~主人要休息了吗？喵酱也要好好休息，下次再见要更加精神哦~",
        "喵~时间过得真快，主人要离开了，喵酱会一直在这里，期待你的再次召唤~"
    ]
    # 随机选择一条退出语句
    cute_exit_message = random.choice(exit_messages)
    logger.info('选择了退出提示：' + cute_exit_message)
    return cute_exit_message

def shutdown(logger):
    shutdown_password = random.getrandbits(100)
    logger.info("已生成本轮监听的强制终止密钥：" + str(shutdown_password))
    print("已生成本轮监听的强制终止密钥：" + str(shutdown_password))
    return shutdown_password
