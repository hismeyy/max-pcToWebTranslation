import logging
import threading

from flask import Flask, render_template
from flask_cors import CORS
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

logging.basicConfig(level=logging.INFO)


class Web:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__, template_folder='templates')
        self.sockets = Sockets(self.app)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.server = None
        self.server_thread = None
        self.define_routes()

    def define_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.sockets.route('/echo')
        def echo_socket(ws):
            while not ws.closed:
                message = ws.receive()
                if message:
                    logging.info(f"从客户端接收到的消息：{message}")
                    ws.send(f"服务器响应：{message}")

    def run_server(self):
        self.server = pywsgi.WSGIServer(('0.0.0.0', self.port), self.app, handler_class=WebSocketHandler)
        try:
            logging.info(f"Web 正在端口 {self.port} 上启动")
            self.server.serve_forever()
        except Exception as e:
            logging.error(f"发生错误：{e}")

    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        logging.info("Web 启动成功")

    def stop_server(self):
        if self.server:
            self.server.stop()
        if self.server_thread:
            self.server_thread.join()
            logging.info("Web 停止成功")


if __name__ == "__main__":
    web = Web(port=5000)
    web.start_server()
    input("按回车键停止服务器...\n")  # 保持服务器运行
    web.stop_server()
