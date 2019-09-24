import socket
import time
import threading

HOST = "127.0.0.1"
PORT = 5000
flag = 1

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(20)
def normal():
    global flag
    while flag == 1:
        client, address = srv.accept()
        for index in range(1,10):
            data = client.recv(2048)
            data_str = data.decode("utf-8")
            result = f"{client}/n{data}/n{address}"
            print(result)
            if not data:
                break
            client.send(data)
    if flag==False:
            print('The while loop is now closing')
            srv.close()

def get_input():
    global flag
    keystrk=input('Press a key \n')
    print('You pressed: ', keystrk)
    flag=False
    print('flag is now:', flag)

n=threading.Thread(target=normal)
i=threading.Thread(target=get_input)
n.start()
i.start()
