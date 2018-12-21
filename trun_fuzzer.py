#!/usr/bin/python

# much <3 for https://zeroaptitude.com/zerodetail/fuzzing-with-boofuzz/
# to do: expand blocks to fuzz all commands within vulnserver and fuzz all commands to find different errors

from boofuzz import *
from sys import exit

target_ip = "X.X.X.X"
target_port = 9999

def main():
    # write logs to .csv file in current directory
    csv_log = open("fuzz_results.csv","wb")
    my_logger = [FuzzLoggerCsv(file_handle=csv_log)]
    # defines port for process_monitor.py on remote machine and commands to be passed to it
    t = Target(connection = SocketConnection(target_ip, target_port, proto='tcp'), procmon=pedrpc.Client(target_ip, 26002), procmon_options = {"proc_name" : "vulnserver.exe", "stop_commands":['wmic process where (name="vulnserver") delete'],"start_commands":['vulnserver.exe'],})
    
    # defines target, logger, and crash threshold, this config will stop the fuzzing after 1 crash
    session = Session(target=t, fuzz_loggers = my_logger, crash_threshold_element = 1)
    s_initialize("Request")
    
    # block which defines data that will be sent during fuzzing attempts
    s_string("TRUN", fuzzable=False)
    s_delim(" ", fuzzable=False, name='space-1')
    s_string("data")

    session.connect(s_get("Request"))
    session.fuzz()

if __name__ == '__main__':
    main()
