# coding=utf-8
import http.server
import io
import os, sys
import threading
import ctypes
import time
#msvc=ctypes.windll.LoadLibrary('kernel32')
sys.path.append(".")
import server as chatserver
def server(protogenesis_request: str) -> (int, str):  # 左边那种东西是一种注释
    tmp = protogenesis_request[protogenesis_request.find("?") + 1:]
    c = {i[0]: i[1] for i in [i.split("=") for i in tmp.split("&")]}  # i在不同作用域中 混用没问题
    try:
        return chatserver.processor(c)
    except (chatserver.INBException,e):
        _=e.args
        
    return (302,"")


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        f = self.send_head()
        if f == None:
            return
        self.copyfile(f, self.wfile)
        f.close()

    def send_head(self):
        i = io.BytesIO()
        if self.path[:19] == "/cgi/chat_server.py":
            tmp = server(self.path[9:])
            self.send_response(tmp[0])
            data = tmp[1]
            self.send_header("Pragma","No-cache")
            self.send_header("Cache-Control","no-cache")
            i.write(bytes(data.encode("gb2312")))  # 在中国貌似浏览器都用的gbk编码 这是微软的锅
        else:
            path = self.translate_path(self.path if self.path != '/' else "/index.html")
            try:
                f = open(path, 'rb')
                self.send_response(200)
                if len(self.path)<2 or ".html"in self.path:
                    self.send_header("Content-type", "text/html")
                elif ".css" in self.path:
                    self.send_header("Content-type", "text/css")
                data = f.read()
                i.write(data)
            except OSError:
                self.send_error(404, self.path + "File not found.\n")
                return None

        i.seek(0)  # 移动光标至初始
        return i

    def log_message(self, format, *args):  # 屏蔽log输出
        pass


if __name__ == "__main__":
    httpd = http.server.HTTPServer(("0.0.0.0", 80), RequestHandler)
    print("Server is running. http://localhost:80 and External network support.")
    httpd.serve_forever(0.2)
