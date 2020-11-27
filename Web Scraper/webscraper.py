import argparse
import socket
import threading
import requests
from bs4 import BeautifulSoup


class Scrap:


    def __init__(self, url):
        self.img_vector = []
        self.p_vector = []
        self.url = url


    def hand_scrap(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")

        self.f_leaves(soup)
        self.img_vector = soup.find_all('img')
        responce = f"{len(self.p_vector)},{len(self.img_vector)}"
        return responce


    def f_leaves(self, soup):
        elements = soup.find_all('p')
        for element in elements:
            if element.find_all() == []:
                self.p_vector.append(element.text)
            else:
                self.f_leaves(element)


class Server:


    def __init__(self, host, port):
        self.host = host
        self.port = port


    def work(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print('Server started')

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.hand, args=(conn, addr))
            thread.start()


    def hand(self, conn, addr):
            print(f'Connected to the {addr}')
            url = self.receive_all(conn)
            print(f'URL : {url}')
            scrap = Scrap(url)
            data = scrap.hand_scrap()
            responce = len(data).to_bytes(10, byteorder='big') + data.encode('utf-8')
            conn.sendall(responce)
            conn.close()
            print(f'Disconnected from the {addr}')


    def receive_all(self, sock):
        msg_len = sock.recv(10)
        msg_len = int.from_bytes(msg_len, byteorder='big')
        msg = sock.recv(msg_len).decode('utf-8')

        return msg


class Client:


    def __init__(self, host, port, url):
        self.host = host
        self.port = port
        if ('https://' not in url):
            self.url = "https://" + url
        else:
            self.url = url


    def work(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        data_len = len(self.url)
        data = data_len.to_bytes(10, byteorder='big') + self.url.encode('utf-8')
        sock.sendall(data)
        responce = self.receive_all(sock)
        p_count, img_count = responce.split(",")
        print(f"The number of images at {self.url} is equal to {img_count}, the number of leaf paragraphs is equal {p_count}")
        sock.close()


    def receive_all(self,sock):
        msg_len=sock.recv(10)
        msg_len = int.from_bytes(msg_len, byteorder='big')
        msg=sock.recv(msg_len).decode('utf-8')
        return msg


if __name__ == '__main__':
    choices = ['client', 'server']
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('role', choices=('client', 'server'), help='Role script will play - server or client')
    parser.add_argument('--host', metavar='host', help='IP / hostname (default IP/hostname is 127.0.0.1)', default="127.0.0.1")
    parser.add_argument('--port', metavar='port', help='TCP port (default port is 1060)', type=int, default=1060)
    parser.add_argument('-p', metavar='page', help='Query URL')

    args = parser.parse_args()
    role = args.role

    if role == "client":
        client = Client(args.host, args.port, args.p)
        client.work()
    elif role == 'server':
        server = Server(args.host, args.port)
        server.work()

