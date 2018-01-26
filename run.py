import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urls import urlpatterns
import controller
import os
import re
import glob


class requesthandlerclass(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def printpage(self, filename, fun_pattern):
        try:
            f_encripted = open(filename, "r").read()
            # print(f_encripted)
            # creating a funtion
            method_to_call = getattr(controller, fun_pattern)
            f_decripted = f_encripted % method_to_call()
            self._set_headers()
            self.wfile.write(f_decripted.encode())
        except:
            self.send_error(404, "File not found " + self.path)

    def getPageData(self, urlpath):
        # print(urlpath)
        # print(urlpatterns)
        for i in range(len(urlpatterns)):
            pattern = urlpatterns[i].split(',')[0].split('\'')[1]
            if (re.match(pattern, urlpath, re.I)):
                htmlfile = urlpatterns[i].split(',')[2].split('\'')[1]
                pattern = urlpatterns[i].split(',')[1].split('.')[-1]
                if htmlfile in os.listdir():
                    self.printpage(htmlfile, pattern)
                    return
                else:
                    self.send_error(404, "File not found " + self.path)
                    return
        self.send_error(404, "File not found " + self.path)

    def do_GET(self):
        self.getPageData(self.path.rsplit("/")[-1])

        # self._set_headers()
        # self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode())


def run(portId):
    try:
        server_address = ('localhost', portId)
        server = HTTPServer(server_address, requesthandlerclass)
        server.serve_forever()
    except KeyboardInterrupt:
        print("you interupted the code")
        server.close_request()


if __name__ == "__main__":
    previewCmp = sys.argv[1]
    if previewCmp == 'preview' and len(sys.argv) == 3:
        portid = int(sys.argv[2].split(':')[-1])
        print("control+c to quit")
        run(portid)
    else:
        print("Wrong input. Try again")
        exit(0)
