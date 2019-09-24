import socket
import threading as th

#print(dir(socket))

HOST = "127.0.0.1"
PORT = 5000

def executor(key):
    try:
        sock = storage[key]
    except KeyError:
        print(f"Key {key} not found")
        return
    try:
        while True:
            data = sock.recv(2048)
            words = data.decode("utf-8").split()
            words.sort()
            if "close" in words:
                break
            response = "/\n".join(words)
            for client, sock in storage.items():
                if client != key:
                    client_sock.send(f"{client[0]}\n".encode("utf-8"))
                    client_sock.send(response.encode("utf-8"))

            sock.send(response.encode("utf-8"))
    except Exception as e:
        print(e)
    finally:
        sock.close()
        del storage[key]



srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(20)
storage = {}
try:
    flag = True
    while flag:
        client, addr = srv.accept()
        storage[addr] = client
        worker = th.thread(executor, addr)
        worker.start()
except Exception as e:
    print(e)
finally:
    srv.close()


