#!/usr/bin/env python3

import socketserver
import threading
import socket
import time
import os

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 21

FILES_DIRECTORY = "pub"


def logging(addr, cmd, arg):
    print(addr, cmd, arg)
    with open("honeypot.log", "a") as f:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write("%s %s:%s: %s %s\n" % (current_time, *map(str, addr), cmd, arg))


def save_file(filename, data):
    if not os.path.isdir(FILES_DIRECTORY):
        os.makedirs(FILES_DIRECTORY)

    base_dir = os.path.dirname(os.path.realpath(__file__))

    filename = "".join(c for c in filename if c.isalnum())
    filename = os.path.join(
        base_dir, FILES_DIRECTORY, time.strftime("%Y_%m_%d__%H_%M_%S__") + filename)
    with open(filename, "wb") as f:
        f.write(data)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle_USER(self, arg):
        self.request.sendall(b"331 User name okay, need password.\r\n")

    def handle_PASS(self, arg):
        self.request.sendall(b"230 User logged in, proceed.\r\n")

    def handle_PWD(self, arg):
        self.request.sendall(b"257 \"/\" created.\r\n")

    def handle_CWD(self, arg):
        self.request.sendall(b"250 Requested file action okay, completed.\r\n")

    def handle_TYPE(self, arg):
        self.request.sendall(b"200 Command okay.\r\n")

    def handle_PASV(self, arg):
        self.ftp_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ftp_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ftp_data.bind((LISTEN_HOST, 0))
        self.ftp_data.listen(1)

        addr, port = self.ftp_data.getsockname()

        self.request.sendall(b"227 Entering Passive Mode (%i,%i,%i,%i,%i,%i).\r\n" % (
            *map(int, addr.split(".")), port // 256, port % 256
        ))

    def handle_LIST(self, arg):
        if self.ftp_data is None:
            self.request.sendall(b"503 Bad sequence of commands.\r\n")
            return

        self.request.sendall(b"150 File status okay; about to open data connection.\r\n")
        sock = self.ftp_data.accept()[0]

        sock.sendall(
            b"-rwxr--r-- 1 vrin vrin 171377 Oct  19 21:58 logo.jpg\r\n"
            b"-rwxr--r-- 1 ms ms 660377 Oct  19 21:58 manual.pdf\r\n"
            b"-rwxr--r-- 1 alze alze 142377 Oct  19 21:58 result2023.doc\r\n"
            b"-rwxr--r-- 1 root pos 3300133 Oct  19 21:58 1ununs000.exe\r\n"
        )

        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        self.ftp_data.close()
        self.request.sendall(b"226 Closing data connection.\r\n")

    def handle_STOR(self, arg):
        if self.ftp_data is None:
            self.request.sendall(b"503 Bad sequence of commands.\r\n")
            return

        self.request.sendall(b"150 Opening ASCII mode data connection for file.\r\n")
        sock = self.ftp_data.accept()[0]

        data = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk

        save_file(arg, data)

        self.ftp_data.close()
        self.request.sendall(b"226 Transfer complete\r\n")

    def handle_SIZE(self, arg):
        self.request.sendall(b"550 Requested action not taken.\r\n")

    def handle_QUIT(self, arg):
        self.request.sendall(b"221 Service closing control connection.\r\n")
        self.close_connection = True

    def handle(self):
        self.request.sendall(b"220 Welcome to FTP Honeypot!\r\n")
        self.close_connection = False
        self.ftp_data = None

        handlers = {
            "USER": self.handle_USER,
            "PASS": self.handle_PASS,
            "LIST": self.handle_LIST,
            "TYPE": self.handle_TYPE,
            "PASV": self.handle_PASV,
            "STOR": self.handle_STOR,
            "SIZE": self.handle_SIZE,
            "QUIT": self.handle_QUIT,
            "PWD": self.handle_PWD,
            "CWD": self.handle_CWD
        }

        while not self.close_connection:
            data = str(self.request.recv(1024), "utf-8").strip().split(" ")
            if data[0] == "":
                continue
            cmd, arg = data[0], data[1] if len(data) > 1 else ""

            logging(self.client_address, cmd, arg)

            if cmd in handlers:
                handlers[cmd](arg)
            else:
                self.request.sendall(b"502 Command not implemented.\r\n")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    ThreadedTCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((LISTEN_HOST, LISTEN_PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server loop running in thread: %s" % server_thread.name)

    server_thread.join()

    server.shutdown()
    server.server_close()
