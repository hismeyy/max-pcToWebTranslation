import os

from Server import Server
from Web import Web
from Win import Win

if __name__ == '__main__':
    # 启动Server线程
    server = Server(port=8765)
    server.start_server()
    # 创建并启动Web线程
    web = Web(port=5000)
    web.start_server()

    # 主线程创建桌面窗口
    # 构建HTML文件的路径
    html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page/index.html')
    url = 'file://' + html_file_path

    win = Win("Max手机翻译", 600, 500, url)
    win.start_pc_win()

    server.stop_server()
    web.stop_server()
