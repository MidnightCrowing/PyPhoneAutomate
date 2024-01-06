from subprocess import PIPE
from subprocess import Popen

process = Popen('adb shell dumpsys battery'.split(), stdout=PIPE)
data, _ = process.communicate()
data_str = data.decode('utf-8')  # 将字节串转换为字符串
lines = data_str.split('\r\n')  # 按行分割字符串

level = None
# 遍历每一行，查找包含 'level' 的行
for line in lines:
    if 'level' in line:
        # 提取 level 的值
        level_str = line.split(':')[-1].strip()
        level = int(level_str)
        break
print(level)
