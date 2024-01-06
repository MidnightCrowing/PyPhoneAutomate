import glob
import os
from datetime import datetime


def rename_images_with_creation_time(directory):
    # 获取目录下所有图片文件的路径
    image_files = glob.glob(os.path.join(directory, '*.jpg')) + glob.glob(os.path.join(directory, '*.png'))

    for file_path in image_files:
        # 获取文件的创建时间
        creation_time = os.path.getctime(file_path)
        # 将创建时间转换为指定格式的字符串
        new_file_name = datetime.fromtimestamp(creation_time).strftime('%Y%m%d_%H%M%S')

        # 保留原始文件的扩展名
        _, ext = os.path.splitext(file_path)

        # 构造新文件名（带序号）
        counter = 1
        new_file_path = os.path.join(directory, f'{new_file_name}_{counter}{ext}')
        while os.path.exists(new_file_path):
            counter += 1
            new_file_path = os.path.join(directory, f'{new_file_name}_{counter}{mark}{ext}')

        # 重命名文件
        os.rename(file_path, new_file_path)

        print(f'Renamed "{file_path}" to "{new_file_path}"')


if __name__ == '__main__':
    """
    说明:
    工具会将该目录下的 *.jpg | *.png 文件的文件名修改为文件创建的时间
    但不会处理多层目录
    如果创建时间重复, 工具会在最后加上序号
    
    例子:
        20231011_185228_1.jpg
        20231011_185310_1.jpg
        20231011_220151_1.jpg
    """
    # TODO 目录路径
    directory_path = r'I:\PyPhoneAutomate\image_data\interface_identify_model\raw\game_interface'
    # TODO 标记
    mark = '1'
    # 调用函数进行重命名
    rename_images_with_creation_time(directory_path)
