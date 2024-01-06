from threading import Thread

from backend import NeuralNetworkControl
from backend import PEControl
from backend import PluginsControl
from .flask_handler import run as run_flask_serve
from .flask_handler import set_control as flask_set_control
from .flask_handler import set_neural_network_control_callbacks
from .websocket_handler import run as run_websocket_serve
from .websocket_handler import set_control as websocket_set_control


class Serve:
    def __init__(
            self,
            pe_control: PEControl,
            plugins_control: PluginsControl,
            neural_network_control: NeuralNetworkControl
    ):
        self.pe_control = pe_control
        flask_set_control(
            pe_control_=pe_control,
            plugins_control_=plugins_control,
            neural_network_control_=neural_network_control
        )
        websocket_set_control(pe_control_=pe_control)

        set_neural_network_control_callbacks()

    @classmethod
    def start(cls, debug=False, host='localhost', flask_port=8001, websocket_port=8002):
        if flask_port == websocket_port:
            raise ValueError("Flask port and WebSocket port cannot be the same. Please use different ports.")

        websocket_thread = Thread(target=run_websocket_serve, kwargs={'host': host, 'port': websocket_port})
        websocket_thread.start()
        # ValueError: signal only works in main thread
        run_flask_serve(host=host, port=flask_port, debug=debug, websocket_port=websocket_port)
