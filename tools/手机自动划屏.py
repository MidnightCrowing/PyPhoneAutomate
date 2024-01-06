import os
from time import sleep
'''
cycle = 1
timeout = 7
while True:
    print('\r', f'划屏中 ({cycle}) ', end='')
    os.system('adb shell input swipe 740 500 740 100')
    os.system('adb shell input swipe 1500 500 1500 100')
    os.system('adb shell input swipe 1920 790 1920 400')
    for i in range(1, timeout):
        print('·', end='')
        sleep(1)
    cycle += 1
'''

cycle = 1
timeout = 7
while True:
    print('\r', f'划屏中 ({cycle}) ', end='')
    os.system('adb shell input swipe 740 1500 740 500')
    for i in range(1, timeout):
        print('·', end='')
        sleep(1)
    cycle += 1
