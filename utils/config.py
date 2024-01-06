from os.path import abspath
from os.path import dirname
from os.path import join

from yaml import load, FullLoader

file_path = abspath(__file__)  # 文件绝对路径
root_path = dirname(dirname(file_path))  # 项目路径
setting_path = join(root_path, 'setting')  # 项目设置目录路径


def load_yaml(path: str):
    """
    :param path: 文件路径
    :return: 文件内容
    """
    with open(path, 'r', encoding='utf-8') as f:
        settings = load(f.read(), Loader=FullLoader)
    return settings


class YamlFiles:
    api_path = join(setting_path, 'api.yaml')
    client_path = join(setting_path, 'client.yaml')
    logging_path = join(setting_path, 'logging.yaml')
    neural_network_path = join(setting_path, 'neural_network.yaml')


class ClientSetting:
    settings = load_yaml(YamlFiles.client_path)

    bitrate = settings['bitrate']
    max_fps = settings['max_fps']


class NeuralNetworkSetting:
    setting = load_yaml(YamlFiles.neural_network_path)

    # ----------> Yolov5 <----------
    yolov5_setting = setting['yolov5']
    yolov5_half_precision = yolov5_setting['half_precision']
    yolov5_device = yolov5_setting['device']
    yolov5_image_size = yolov5_setting['image_size']
    yolov5_confidence_threshold = yolov5_setting['confidence_threshold']
    yolov5_iou_threshold = yolov5_setting['iou_threshold']
    yolov5_max_detections = yolov5_setting['max_detections']
    yolov5_class_labels = yolov5_setting['class_labels']
    yolov5_agnostic_nms = yolov5_setting['agnostic_nms']
    yolov5_augment = yolov5_setting['augment']
    yolov5_visualize = yolov5_setting['visualize']
