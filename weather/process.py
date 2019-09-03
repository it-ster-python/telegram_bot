import multipprocessing as mp
import threading as th
import time

def executor(index, res=[]):
    print("Executor start", index)
