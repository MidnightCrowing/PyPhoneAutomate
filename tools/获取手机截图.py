import io
import os
import subprocess
from sys import exc_info
from threading import Thread
from time import sleep, strftime
from tkinter import ACTIVE, DISABLED

from PIL import Image, UnidentifiedImageError
from ttkbootstrap import Window, Frame, Radiobutton, Button, Label, Spinbox, IntVar, READONLY
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification


class MyWindow:
    def __init__(self):
        self.screenshots = False

        self.root = Window(title=os.path.basename(__file__), themename='darkly')
        self.root.resizable(False, False)

        self.frame1 = Frame(self.root)
        self.frame1.pack(side='top', fill='x', ipady=20)

        self.open_folder_btn = Button(self.frame1, text='打开文件夹', style='secondary')
        self.open_folder_btn.configure(command=self.open_folder)
        self.open_folder_btn.pack(side='right', padx=30, ipadx=30)

        self.frame2 = Frame(self.root)
        self.frame2.pack(side='top', padx=50, ipadx=40, ipady=15)

        self.var = IntVar()

        self.chk1 = Radiobutton(self.frame2, text='自动', variable=self.var, value=1, style='warning')
        self.chk1.configure(command=self.chk1_func)
        self.chk1.grid(row=1, column=1, pady=10)

        self.chk1_btn = Button(self.frame2, text='开始', style='success')
        self.chk1_btn.configure(command=self.chk1_btn_start_func)
        self.chk1_btn.grid(row=2, column=2, padx=20, ipadx=50)

        self.spin_lab = Label(self.frame2, text='等待时长:')
        self.spin_lab.grid(row=2, column=3)

        self.chk1_spin = Spinbox(self.frame2, width=2, justify='center', state=READONLY, style='success')
        self.chk1_spin.configure(from_=0, to=60)
        self.chk1_spin.grid(row=2, column=4, padx=10)

        self.chk2 = Radiobutton(self.frame2, text='手动', variable=self.var, value=2, style='warning')
        self.chk2.configure(command=self.chk2_func)
        self.chk2.grid(row=4, column=1, pady=10)

        self.chk2_btn = Button(self.frame2, text='截图', style='success-outline')
        self.chk2_btn.configure(command=self.chk2_btn_func)
        self.chk2_btn.grid(row=5, column=2, padx=20, ipadx=50)

        self.init_var()

    def init_var(self):
        self.var.set(1)
        self.chk1_func()
        self.chk1_spin.set(0)

    def open_folder(self):
        try:
            os.startfile(screenshot_dir)
        except FileNotFoundError:
            _, message, _ = exc_info()
            self.meet_error('FileNotFoundError', f'{message}')

    def chk1_func(self):
        self.chk1_btn.configure(state=ACTIVE)
        # noinspection PyArgumentList
        self.spin_lab.configure(state=ACTIVE, bootstyle='light')
        # noinspection PyArgumentList
        self.chk1_spin.configure(state=READONLY, bootstyle='light')
        self.chk2_btn.configure(state=DISABLED)

    def chk2_func(self):
        self.chk1_btn.configure(state=DISABLED)
        # noinspection PyArgumentList
        self.spin_lab.config(state=DISABLED, bootstyle='dark')
        # noinspection PyArgumentList
        self.chk1_spin.configure(state=DISABLED, bootstyle='dark')
        self.chk2_btn.configure(state=ACTIVE)

        if self.screenshots:
            self.chk1_btn_stop_func()

    def chk1_btn_start_func(self):
        self.screenshots = True
        # noinspection PyArgumentList
        self.chk1_btn.config(text='停止', command=self.chk1_btn_stop_func, bootstyle='success-link')

        Thread(target=self.keep_screenshots).start()

    def chk1_btn_stop_func(self):
        self.screenshots = False
        # noinspection PyArgumentList
        self.chk1_btn.config(text='开始', command=self.chk1_btn_start_func, bootstyle='success')

    def keep_screenshots(self):
        while self.screenshots:
            self.capture_screenshots()
            sleep(int(self.chk1_spin.get()))

    def chk2_btn_func(self):
        self.capture_screenshots()
        ToastNotification(title='手机截图', message='截图成功', duration=1000, bootstyle='dark').show_toast()

    def capture_screenshots(self):
        current_time = strftime('%Y%m%d_%H%M%S')
        screenshot_file = os.path.join(screenshot_dir, f'{current_time}.jpg')
        # 执行ADB截图命令
        adb_command = 'adb exec-out screencap -p'
        process = subprocess.Popen(adb_command.split(), stdout=subprocess.PIPE)
        # 读取截图数据s
        screenshot_data, _ = process.communicate()
        # 将截图数据加载到PIL图像对象中
        try:
            image = Image.open(io.BytesIO(screenshot_data))
        except UnidentifiedImageError:
            _, message, _ = exc_info()
            self.meet_error('PIL.UnidentifiedImageError', str(message))
        else:
            # 丢弃掉alpha通道的信息
            image = image.convert('RGB')
            # 使用PIL库打开截图并进行缩小
            # image = image.resize((int(image.width * 0.15), int(image.height * 0.15)))
            # 保存截图
            try:
                image.save(screenshot_file)
            except FileNotFoundError:
                _, message, _ = exc_info()
                self.meet_error('FileNotFoundError', f'{message}')

    def meet_error(self, title: str, message: str):
        if self.screenshots:
            self.chk1_btn_stop_func()
        try:
            Messagebox.show_error(title=title, message=message, alert=True)
        except RuntimeError:
            self.var.set(2)
            self.chk2_func()

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    # TODO 截图保存路径
    screenshot_dir = r'I:\PyPhoneAutomate\image_cache'

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    win = MyWindow()
    win.mainloop()
