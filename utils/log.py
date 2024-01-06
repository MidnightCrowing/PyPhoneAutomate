import logging
from os import mkdir, chdir
from os.path import exists, dirname, abspath
from time import strftime, localtime

BASE_DIR = dirname(dirname(abspath(__file__)))  # 项目根目录
chdir(BASE_DIR)  # 更改当前工作路径

# 检测log路径是否存在
if not exists('log'):
    mkdir('log')

logger = logging.getLogger(__name__)  # logger

# 输出格式设置
formatter = logging.Formatter('\n%(asctime)s - %(filename)s[line:%(lineno)d] - process:%(process)d - thread:%('
                              'threadName)s (id: %(thread)d) - function: %(funcName)s - %(levelname)s:'
                              '\n%(message)s')

# -----------------------------------------------------------------------------------
# DEBUG: 程序调试bug时使用
# INFO: 程序正常运行时使用
# WARNING: 程序未按预期运行时使用，但并不是错误，如:用户登录密码错误
# ERROR: 程序出错误时使用，如:IO操作失败
# CRITICAL: 特别严重的问题，导致程序不能再继续运行时使用，如:磁盘空间为空，一般很少使用
# -----------------------------------------------------------------------------------

# 文件输出设置
file_handler = logging.FileHandler(f'log/{strftime("%Y-%m-%d %H：%M：%S", localtime())}.txt')
file_handler.setLevel(level=logging.DEBUG)  # 设置控制台输出级别
file_handler.setFormatter(formatter)

# 控制台输出设置
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)  # 设置文件输出级别
stream_handler.setFormatter(formatter)

logger.setLevel(level=logging.DEBUG)  # 设置收集级别
logger.addHandler(file_handler)  # 添加进log设置中
logger.addHandler(stream_handler)
