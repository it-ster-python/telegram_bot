import time
from threading import Thread

def block(block_time):
    print("start")
    time.sleep(block_time)
    print("finish, index")

if__name__ == '__main__':
for index in range(5):
    worker = Thread(target=block, args = (60, index))
