import json
import os
import time


# read messages from node
INPUT_PIPE_PATH="N2P"
# send responses to node
OUTPUT_PIPE_PATH="P2N"


# courtesy https://www.ravenblack.net/random/surreal.html
response = {
    'name':'response',
    'text': "Is it a peacock? Is it a net curtain? No, it's hair-Man! More silly knees-bent running-about than a fatal street map, able to oven-roast"
}

def loop():
    control = os.open(INPUT_PIPE_PATH, os.O_RDONLY | os.O_NONBLOCK)

    while True:
        try:
            # XXX need to buffer this for messages > 512 bytes
            _cmd = os.read(control, 512)
            if _cmd:
                print(">>> got a message")
                print(_cmd)

                # simulate a long process to simulate surreal responses
                print(">>> generating surreal response, please wait!")
                time.sleep(10)
                response_data = bytes(json.dumps(response), 'utf-8')
                print(response_data, type(response_data))

                print(">>> trying to send a response")
                fd = os.open(OUTPUT_PIPE_PATH, os.O_WRONLY | os.O_NONBLOCK)
                print(fd) # XXX some error checking maybe
                os.write(fd, response_data)
                os.close(fd)
                print('>>> ok!')

        except Exception as e:
            print("Exception trying to read named pipe:{}".format(e))

        time.sleep(0.5)

if __name__ == '__main__':
    loop()
