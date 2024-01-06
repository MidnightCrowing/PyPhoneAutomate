from backend import pe_control, plugins_control, neural_network_control
from services import Serve

if __name__ == '__main__':
    pe_control.set_device(pe_control.get_devices_list()[0])
    serve = Serve(pe_control=pe_control, plugins_control=plugins_control, neural_network_control=neural_network_control)
    serve.start()  # 启动服务
