from threading import Thread, Event


class MyThread(Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = Event()  # 结束标志
        self._recover_event = Event()  # 暂停标志
        self._recover_event.set()

    def wait(self):
        """ 挂起 """
        self._recover_event.wait()  # 如果设置暂停状态, 则一直等待至其状态解除

    def pause(self):
        """ 暂停 """
        self._recover_event.clear()

    def recover(self):
        """ 恢复 """
        self._recover_event.set()

    def stop(self):
        """ 结束 """
        if self.paused():  # 如果处于暂停状态, 则会一直等待, 无法检测结束标志位
            self.recover()
        self._stop_event.set()

    def paused(self) -> bool:
        """ 判断线程是否处于暂停状态 """
        return not self._recover_event.is_set()

    def stopped(self) -> bool:
        """ 判断线程是否处于终止状态 """
        return self._stop_event.is_set()
