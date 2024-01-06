from random import randint
from typing import Literal
from typing import Optional

from flask import Flask
from flask import Response
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from flask_cors import CORS
from flask_socketio import SocketIO

from backend import NeuralNetworkControl
from backend import PEControl
from backend import PluginsControl
from utils.exceptions import NoPluginThread

app = Flask(__name__, template_folder='../app', static_folder='../app/static')
# Enable CORS for all routes of the Flask and WebSocket app
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有源进行访问
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')  # 允许自定义请求头
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')  # 允许请求的方法
    return response


@app.route('/')
def index():
    # 获取多个 CSS 和 JS 文件的 URL
    css_urls = [url_for('static', filename='css/body.css'),
                url_for('static', filename='css/content-box.css'),
                url_for('static', filename='css/messages.css'),
                url_for('static', filename='css/right-side.css'),
                url_for('static', filename='css/root-container.css'),
                url_for('static', filename='css/load-circle.css'),
                url_for('static', filename='css/screen.css')]
    js_urls = [url_for('static', filename='js/libs/jquery-3.6.4.min.js'),
               url_for('static', filename='js/libs/socket.io.js'),
               url_for('static', filename='js/script.js')]

    return render_template('index.html', css_urls=css_urls, js_urls=js_urls)


@app.route('/get_config', methods=['GET'])
def get_config():
    json_data = {
        "flask": f"http://{host_}:{flask_port_}/",
        "websockets": f"ws://{host_}:{websocket_port_}"
    }
    return jsonify(json_data)


def set_control(
        pe_control_: PEControl,
        plugins_control_: PluginsControl,
        neural_network_control_: NeuralNetworkControl
):
    global pe_control, plugins_control, neural_network_control
    pe_control = pe_control_
    plugins_control = plugins_control_
    neural_network_control = neural_network_control_


class StartPluginMessages:
    @staticmethod
    def get_msg_id():
        # 生成一个4位数的随机数字字符串
        return ''.join(str(randint(0, 9)) for _ in range(4))

    def set_neural_network_control_callbacks(self):
        callbacks = {
            'load_tensorflow_framework_start': self.load_start('加载tensorflow框架'),
            'load_tensorflow_model_start': self.load_start('加载tensorflow模型'),
            'load_yolov5_framework_start': self.load_start('加载yolov5框架'),
            'load_yolov5_setting_start': self.load_start('加载yolov5设置'),
            'load_yolov5_model_start': self.load_start('加载yolov5模型'),
            'load_sklearn_model_start': self.load_start('加载sklearn模型'),
            'load_tensorflow_framework_end': self.load_end,
            'load_tensorflow_model_end': self.load_end,
            'load_yolov5_framework_end': self.load_end,
            'load_yolov5_setting_end': self.load_end,
            'load_yolov5_model_end': self.load_end,
            'load_sklearn_model_end': self.load_end
        }
        neural_network_control.set_callback_function(callbacks)

    def load_start(self, message):
        def start(name=None):
            msg_id = self.get_msg_id()
            self.seed_message(msg_id, message=message, name=name, state='start')
            return msg_id

        return start

    def load_end(self, msg_id):
        self.seed_message(msg_id, state='finish')

    @staticmethod
    def seed_message(msg_id: str, state: Literal['start', 'finish'], message=None, name=None):
        socketio.emit('message', {'msgId': msg_id, 'state': state, 'message': message, 'name': name})


# 获取插件列表
@app.route('/get_plugins_list', methods=['GET'])
def get_plugins_list():
    plugins = plugins_control.get_plugins_list()
    # 发送列表数据
    return jsonify(plugins)


# 获取插件图标
@app.route('/get_plugin_icon/<name>', methods=['GET'])
def get_plugin_icon(name: str):
    try:
        image_path = plugins_control.get_icon_path(name)
    except FileNotFoundError:
        # 如果文件不存在，返回HTTP 404错误
        abort(404)
    else:
        # 发送icon数据
        return send_file(image_path, mimetype='image/x-icon')


# 获取当前使用的插件名
@app.route('/get_local_plugin_name', methods=['GET'])
def get_local_plugin_name():
    name = plugins_control.get_local_plugin_name()
    # 发送字符串数据
    return Response(name, content_type='text/plain')


# 获取当前管理器的状态
@app.route('/get_plugin_control_state', methods=['GET'])
def get_plugin_control_state():
    state = plugins_control.get_state()
    return jsonify(state)


# 加载插件
@app.route('/load_plugin', methods=['POST'])
def load_plugin():
    # 获取POST请求中的表单数据
    name = request.form.get('name')
    plugins_control.set_local_plugin(name)


# 运行线程任务
@socketio.on('start_plugin')
def start_plugin(data):
    name = data['name']
    result = plugins_control.start(plugin=name)

    if result:
        # Sending a message to the client using emit
        socketio.emit('message', {'result': True})
    else:
        # Sending an error message with status code 400
        socketio.emit('message', {'result': False, 'warning': '后端处理失败，无法运行线程任务，请检查原因'}, status=400)


# 暂停线程任务
@app.route('/pause_plugin', methods=['POST'])
def pause_plugin():
    try:
        result = plugins_control.pause()
    except NoPluginThread:
        # 返回 HTTP 400 Bad Request 状态码，并包含中文警告消息
        return jsonify({'result': False, 'error': 'NoPluginThread', 'message': '没有插件线程，请检查配置'}), 400
    else:
        if result:
            # 返回 True 表示成功
            return jsonify({'result': True})
        else:
            # 处理失败，返回状态码 400 Bad Request 和警告消息
            return jsonify({'result': False, 'warning': '后端处理失败，无法暂停线程任务，请检查原因'}), 400


# 恢复线程任务
@app.route('/recover_plugin', methods=['POST'])
def recover_plugin():
    try:
        result = plugins_control.recover()
    except NoPluginThread:
        # 返回 HTTP 400 Bad Request 状态码，并包含中文警告消息
        return jsonify({'result': False, 'error': 'NoPluginThread', 'message': '没有插件线程，请检查配置'}), 400
    else:
        if result:
            # 返回 True 表示成功
            return jsonify({'result': True})
        else:
            # 处理失败，返回状态码 400 Bad Request 和警告消息
            return jsonify({'result': False, 'warning': '后端处理失败，无法恢复线程任务，请检查原因'}), 400


# 结束线程任务
@app.route('/stop_plugin', methods=['POST'])
def stop_plugin():
    try:
        result = plugins_control.stop()
    except NoPluginThread:
        # 返回 HTTP 400 Bad Request 状态码，并包含中文警告消息
        return jsonify({'result': False, 'error': 'NoPluginThread', 'message': '没有插件线程，请检查配置'}), 400
    else:
        if result:
            # 返回 True 表示成功
            return jsonify({'result': True})
        else:
            # 处理失败，返回状态码 400 Bad Request 和警告消息
            return jsonify({'result': False, 'warning': '后端处理失败，无法结束线程任务，请检查原因'}), 400


def run(host, port, websocket_port, debug=False):
    global host_, flask_port_, websocket_port_
    host_ = host
    flask_port_ = port
    websocket_port_ = websocket_port

    socketio.run(app, debug=debug, port=port, host=host, use_reloader=False, allow_unsafe_werkzeug=True)


pe_control: Optional[PEControl] = None
plugins_control: Optional[PluginsControl] = None
neural_network_control: Optional[NeuralNetworkControl] = None
start_plugin_messages = StartPluginMessages()
set_neural_network_control_callbacks = start_plugin_messages.set_neural_network_control_callbacks
host_: Optional[str] = None
flask_port_: Optional[int] = None
websocket_port_: Optional[int] = None
