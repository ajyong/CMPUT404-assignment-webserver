import SocketServer
from time import gmtime, strftime
from os import path

# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.full_response = ""
        self.message_body = ""
        self.status_line = ""
        self.content_type = ""
        self.content_length = "Content-Length: "

        self.data = self.request.recv(1024).strip()

        request_lines = self.data.splitlines()
        first_line_data = request_lines[0].split()

        if first_line_data[0] != "GET":
            self.status_line = "HTTP/1.1 501 NOT IMPLEMENTED\n"
            self.content_type = "Content-Type: text/html\n"
            self.message_body = "<html><body>HTTP/1.1 501 NOT IMPLEMENTED"
                "</body></html>\n"
        elif first_line_data[1].endswith("/"):
            requested_file_path = os.getcwd() + first_line_data[1] + "/index.html"
            if os.path.isfile(requested_file_path):
                self.status_line = "HTTP/1.1 200 OK\n"
                file = open(requested_file_path)

                self.message_body = file.read()
                self.content_length = getsize(requested_file_path)
            else:
                self.status_line = "HTTP/1.1 404 NOT FOUND\n"
        else:
            self.status_line = "HTTP/1.1 200 OK\n"
            self.message_body = self.data

        self.content_length += str(len(self.message_body)) + "\n"
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(self.data.upper())
        self.request.sendall(self.status_line + self.get_datetime() +
            self.content_type + self.content_length + "\n" + self.message_body
            + "\n")

    def get_datetime(self):
        return "Date: " + strftime("%a, %d %b %Y %X GMT", gmtime()) + "\n"

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
