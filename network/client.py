import socket
import fcntl
import socket
import select
import threading as th
import os

HOST = "127.168.4.182"
PORT = 5000

user = input("Введите логин:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((HOST,PORT))
client.send(user.encode("utf-8"))
while True:
    message = input("Введите сообщение:")
    data = f"User:{user}\r\n{message}\n"
    try:
        client.send(data.encode("utf-8"))
    except Exception as e:
        print(e)
    try:
        request = client.recv(1024)
    except Exception as e:
        print(e)
    print(request.decode("utf-8"))
