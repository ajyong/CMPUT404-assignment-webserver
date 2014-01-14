import SocketServer
from time import gmtime, strftime

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
        full_response = ""
        message_body = ""
        status_line = "HTTP/1.1 200 OK\n"
        date = "Date: " + strftime("%a, %d %b %Y %X GMT", gmtime()) + "\n"
        content_type = "Content-Type: text/plain\n"
        content_length = "Content-Length: "
        self.data = self.request.recv(1024).strip()
        request_lines = self.data.splitlines()
        message_body = request_lines[0]
        first_line_data = request_lines[0].split()
        if first_line_data[0] != "GET":
            status_line = "HTTP/1.1 501 NOT IMPLEMENTED\n"
            message_body = "HTTP/1.1 501 NOT IMPLEMENTED"
        content_length += str(len(message_body)) + "\n"
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(self.data.upper())
        self.request.sendall(status_line + date + content_type + content_length
            + "\n" + message_body + "\n")

    def __get_datetime(self):
        return "Date: " + strftime("%a, %d %b %Y %X GMT", gmtime()) + "\n"

    def respond_not_implemented(self):
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
