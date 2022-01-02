# Thread Test

```python
from threading import Thread

import time


flag = True

def Tread_from_pair():
    i = 0
    while flag:
        print("read: ", i)
        i = i+1
        time.sleep(1)
    print("Tread_from_pair end")

def Twrite_to_pair():
    i = 0
    while flag:
        print("write: ", i)
        i = i+1
        time.sleep(1)
    print("Twrite_to_pair end")

def main():
    try:
        td1 = Thread(target = Tread_from_pair)
        td2 = Thread(target = Twrite_to_pair)

        td1.start()
        td2.start()
    except:
        print("start thread fatal")

    return

if __name__ == "__main__":
    
    main()
    try:
        while True:
            pass
        
    except KeyboardInterrupt:
        print("main end")
        flag = False
    


```