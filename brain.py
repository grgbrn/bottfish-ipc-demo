import json
import os
import time

def loop():
    control = os.open("input", os.O_RDONLY | os.O_NONBLOCK);

    while True:
        try:
            _cmd = os.read(control, 80)
            if _cmd:
                print(">>> got a message")
                print(_cmd)

        except Exception as e:
            print("Exception trying to read named pipe:{}".format(e))

        time.sleep(0.5)

if __name__ == '__main__':
    loop()
