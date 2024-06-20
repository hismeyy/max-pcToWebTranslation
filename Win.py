import webview


class Api:
    def __init__(self):
        pass


class Win:
    api = Api()

    def __init__(self, win_name, win_width, win_height, win_url):
        self.win_name = win_name
        self.win_width = win_width
        self.win_height = win_height
        self.win_url = win_url

    def start_pc_win(self):
        win = webview.create_window(
            self.win_name,
            url=self.win_url,
            js_api=self.api,
            width=self.win_width,
            height=self.win_height
        )
        print(f"log:PC窗口启动成功，{win}")
        webview.start(debug=True)
        # webview.start()
