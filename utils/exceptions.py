class CustomError(Exception):
    """ 自定义错误 """

    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


# --------------------------------------------------
# DeviceControlError
# --------------------------------------------------


class DeviceControlError(CustomError):
    pass


class DeviceDeviceChooseError(DeviceControlError):
    pass


class DeviceBatteryInfoError(DeviceControlError):
    pass


class DeviceScreenshotError(DeviceControlError):
    pass


# --------------------------------------------------
# PluginsControlError
# --------------------------------------------------


class NoChoosePlugin(CustomError):
    pass


class NoPluginThread(CustomError):
    pass
