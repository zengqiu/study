#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 取代 netcat

import os
import sys
import struct
import socket
import getopt
import threading
import subprocess

# Define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def run_command(command):
    """This runs a command and returns the output"""
    command = command.rstrip()    # Trim the newline
    # Run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    
    return output    # Send the output back to the client

def client_handler(client_socket):
    """This handles incoming client connections"""
    global upload
    global execute
    global command

    opt = client_socket.recv(2)

    if opt == '-e':
        while True:
            data = client_socket.recv(1024)
            execute += data
            if len(data) < 1024:
                break
                
        # Check for command execution
        if len(execute):
            output = run_command(execute)    # Run the command
            # print output
            client_socket.send(output)
        execute = ""
        client_socket.close()
    
    if opt == '-u':
        fileinfo_size = struct.calcsize('128sI')
        try:
            fhead = client_socket.recv(fileinfo_size)
            filename, filesize = struct.unpack('128sI', fhead)
            upload_destination = 'upload_' + filename.strip('\00')
            # Check for upload
            if len(upload_destination):
                # Read in all of the bytes and write to our destination
                filedata = ""
                restsize = filesize 
                # Keep reading data until none is available
                while True:
                    if restsize > 1024:
                        filedata += client_socket.recv(1024)
                    else:
                        filedata += client_socket.recv(restsize)
                        break
                    restsize = filesize - len(filedata)    # 计算剩余数据包大小
                    if restsize <= 0:
                        break
                try:
                    # Now we take these bytes and try to write them out
                    fp = open(upload_destination, "wb")
                    fp.write(filedata)
                    fp.close()
                    
                    # Acknowledge that we wrote the file out
                    client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
                except Exception, e:
                    print e
                    client_socket.send("Failed to save file to %s\r\n" % upload_destination)
        except Exception, e:
            print e
            client_socket.close()

    if opt == '-c':
        # Now we go into another loop if a command shell was requested
        if command:
            while True:
                client_socket.send("<BHP:#> ")    # Show a simple prompt
                
                # Now we receive until we see a linefeed (enter key)
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024)
        
                response = run_command(cmd_buffer)    # Execute the valid command and send back the results
                client_socket.send(response)    # Send back the response

def server_loop():
    """This is for incoming connections"""
    global target
    global port
    
    # If no target is defined we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((target, port))
    server.listen(5)        
    
    while True:
        client_socket, addr = server.accept()
        # Spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()
                
def client_sender(buffer):
    """Send data to server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target, port))    # Connect to our target host
        
        # If we detect input from stdin send it 
        # If not we are going to wait for the user to punch some in
        if len(buffer):
            client.sendall(buffer)

        if len(execute) or len(upload_destination):
            recv_len = 1
            response = ""
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                
                if recv_len < 4096:
                    break
            print response,
            client.close()
        else:
            print 'c'
            # Now wait for data back
            while True:
                recv_len = 1
                response = ""
                
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    
                    if recv_len < 4096:
                        break
                print response,
                
                buffer = raw_input("")    # Wait for more input
                buffer += "\n"                        
                
                client.send(buffer)    # Send it off
    except:
        print "[*] Exception! Exiting."
        client.close()    # Teardown the connection

def usage():
    print "Netcat Replacement"
    print
    print "Usage: bh_net.py -t target_host -p port"
    print "-l --listen                - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run   - execute the given file upon receiving a connection"
    print "-c --command               - initialize a command shell"
    print "-u --upload=destination    - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples:"
    print "./bhp_net.py -p 5555 -l -c"
    print "./bhp_net.py -t 192.168.0.1 -p 5555 -c"
    print "./bhp_net.py -t 192.168.0.1 -p 5555 -u c:/target.exe"
    print "./bhp_net.py -t 192.168.0.1 -p 5555 -e \"cat /etc/passwd\""
    print "echo 'GET / HTTP/1.1\r\nHost: www.v2ex.com\r\n\r\n' | ./bhp_net.py -t www.v2ex.com -p 80"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    
    # Read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
    
    # Are we going to listen or just send data from stdin
    # 设置命令前两个字符为操作命令
    if not listen and len(target) and port > 0:
        if len(execute):
            data = '-e' + execute
        elif len(upload_destination):
            filename = os.path.split(upload_destination)[-1]
            fileinfo_size = struct.calcsize('128sI')    # 编码格式大小
            fhead = struct.pack('128sI', filename, os.stat(upload_destination).st_size)    # 按照规则进行打包
            fp = open(upload_destination, 'rb')
            filedata = fp.read()
            fp.close()
            data = '-u' + fhead + filedata
        elif command:
            # Read in the buffer from the commandline
            # This will block, so send CTRL-D if not sending input to stdin
            buffer = sys.stdin.read()
            data = '-c' + buffer    # Send data off
        else:
            data = sys.stdin.read()
        client_sender(data)
    
    # We are going to listen
    if listen:
        server_loop()

main()