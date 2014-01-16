import mimetypes
import os
import SocketServer
from time import gmtime, strftime

# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Aaron Yong
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
    def get_datetime(self):
        return "Date: " + strftime("%a, %d %b %Y %X GMT", gmtime()) + "\n"

    def handle(self):
        self.content_length = "Content-Length: "
        self.content_type = "Content-Type: "
        self.location = ""
        self.message_body = ""
        self.status_line = "HTTP/1.1 "

        # We check against this path to ensure we only serve files within the
        # www folder.
        self.www_path = os.path.join(os.getcwd(), "www")

        self.data = self.request.recv(1024).strip()
        request_lines = self.data.splitlines()
        first_line_data = request_lines[0].split()

        if first_line_data[0] != "GET":
            self.status_line += "501 Not Implemented\n"
            self.content_type += "text/html\n"
            self.message_body = "<html><body><h1>501 NOT IMPLEMENTED" \
                                "</h1></body></html>\n"
        else:
            requested_path = os.path.normpath(os.path.join(self.www_path +
                                              first_line_data[1]))

            # For requests ending in "/", append index.html to the end of the
            # requested file path.
            if first_line_data[1].endswith("/"):
                requested_path = os.path.join(requested_path, "index.html")

            # If requested path is a file and is contained in ./www, read from
            # it and set as response's message body.
            if (os.path.isfile(requested_path) and
                    requested_path.startswith(self.www_path)):

                 # Set the mimetypes depending on the request
                if requested_path.endswith(".html"):
                    self.content_type += "text/html\n"
                elif requested_path.endswith(".css"):
                    self.content_type += "text/css\n"
                else:
                    self.content_type += "text/plain\n"

                self.status_line += "200 OK\n"

                file = open(requested_path)
                self.message_body = file.read()
                file.close()

            # If requested path is a directory and is contained in ./www,
            # send a redirect response with a trailing slash appended to the
            # original request URL.
            elif (os.path.isdir(requested_path) and
                    requested_path.startswith(self.www_path)):
                self.status_line += "301 Moved Permanently\n"
                self.content_type += "text/html\n"
                self.location = "Location: " + first_line_data[1] + "/\n"
                self.message_body = "<html><body><h1>310 MOVED PERMANENTLY" \
                                    "</h1><a href=\"" + first_line_data[1] + \
                                    "/" + "\">Click to get redirected</a>" \
                                    "</body></html>\n"

            # Otherwise, construct a 404 not found response.
            else:
                self.status_line += "404 Not Found\n"
                self.content_type += "text/html\n"
                self.message_body = "<html><body><h1>404 NOT FOUND" \
                                    "</h1></body></html>\n"

        # Calculate the content length of the message body
        self.content_length = self.content_length + \
                              str(len(self.message_body)) + "\n\n"

        # Send out the response
        self.request.sendall(self.status_line + self.get_datetime() +
                             self.location + self.content_type +
                             self.content_length + self.message_body)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
