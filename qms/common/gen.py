import time
import random

def get_uuid():
    t=time.time()
    nowTime = lambda: int(round(time.time() * 1000))+random.randint(1,9999)
    temp=str(nowTime())
    ret=int(temp[4:])
    return ret