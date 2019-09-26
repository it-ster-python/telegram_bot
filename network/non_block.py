import socket
import fcntl
import socket
import select
import threading as th
import os



HOST = "127.168.4.182"
PORT = 5000
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(20)
fcntl.fcntl(srv, fcntl.LOCK_NB)
storage = {srv:(HOST, PORT, "SERVER")}
try:
    work = True
    while work:
        rlist, wlist, xlist = select.select(
            list(storage.keys()), 
            list(storage.keys()),
            list(storage.keys())
            )
        wlist.remove(srv)
        for sock in rlist:
            if sock !=srv:
                data = sock.recv(2048)
                user_data, message = data.decode("utf-8").split("\r\n")

                user_type, user_name = user_data.split(":")
                chat_message = f"{user_type} {username} сказал:\n{message}"
                send_list = wlist[:]
                worker = th.Thread(target = writer, args = (send_list.remove(sock),message,))
                worker.start()
                wlist.remove(sock)
            else:
                client, addr = srv.accept()
                fcntl.fcntl(client, fcntl.LOCK_NB)
                try:
                    login = client.recv(1024)
                except ConnectionResetError:
                    client.close()
                else:
                    data = addr + (login.decode("utf-8"),)
                    storage[client] = data
finally:
    srv.close()

