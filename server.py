#  coding: utf-8 
import socketserver
import os

# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Warren Lim
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        serve_dir = "./www/"
        http_version = "HTTP/1.1 "
        status = ""
        location = ""
        content_type = ""
        res_html = ""

        split_data = self.data.split()
        req_method = split_data[0].decode("utf-8")
        req_path = split_data[1].decode("utf-8")

        correct_method = True
        if req_method != "GET":
            status = "405 Not Allowed\r\n"
            res_html = "<p>405 Not Allowed</p>"
            correct_method = False
        if correct_method:
            if req_path.endswith("/"): req_path += "index.html"
            if os.path.isdir(serve_dir + req_path) and not req_path.endswith("/"):
                status = "301 Moved Permanently\r\n"
                location = f"Location: {req_path}/\r\n"
                content_type = "Content-Type:text/html\r\n"
                res_html = f"<h1>301 Moved Permanently</h1>The document has moved <a href='{req_path}/'>here</a>."
                req_path += "/"
            
            elif os.path.isfile(serve_dir + req_path) and "../" not in req_path:
                with open(serve_dir + req_path) as file:
                    status = "200 OK\r\n"
                    if req_path.endswith(".css"): content_type = "Content-Type:text/css\r\n"
                    else: content_type = "Content-Type:text/html\r\n"
                    res_html = file.read()
            else:
                status = "404 Not Found\r\n"
                res_html = "<p>404 Not Found</p>"
        
        response = http_version + status + location + content_type + "\n" + res_html
        response = response.encode("utf-8")
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
