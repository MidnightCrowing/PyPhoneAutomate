from backend import pe_control, plugins_control
from services import Serve

if __name__ == '__main__':
    pe_list = pe_control.get_devices_list()
    pe_control.set_device(pe_list[0])
    plugins_list = plugins_control.get_plugins_list()
    plugins_control.start(plugins_list[0], sleep_time=1)

    # serve = Serve(pe_control=pe_control, plugins_control=plugins_control)
    # serve.start()
