# -*- coding: utf-8 -*-

# 把本地端口转发到远程主机

import argparse
import asyncore
import socket

LOCAL_SERVER_HOST = 'localhost'
REMOTE_SERVER_HOST = 'www.baidu.com'
BUFSIZE = 4096

class PortForwarder(asyncore.dispatcher):
    def __init__(self, localip, localport, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.localport = localport
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((localip, localport))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        print "Connected to: ", addr
        Sender(Receiver(conn), self.localport, self.remoteip, self.remoteport)

class Receiver(asyncore.dispatcher):
    """接受本地请求数据并发送给远程主机"""
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = ''    # 保存来自远程主机的数据
        self.to_remote_buffer = ''      # 保存本地请求数据
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        """接受本地请求"""
        read = self.recv(BUFSIZE)
        self.to_remote_buffer += read
        print 'Receiver read: ', self.to_remote_buffer

    def writable(self):
        """判断是否有来自远程主机的数据（如有则调用 handle_write）"""
        return (len(self.from_remote_buffer) > 0)

    def handle_write(self):
        """发送来自远程主机的数据给本地主机"""
        sent = self.send(self.from_remote_buffer)
        self.from_remote_buffer = self.from_remote_buffer[sent:]
        print 'Receiver sent: ', sent
        
    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()

class Sender(asyncore.dispatcher):
    """接受远程主机数据并发送本地请求数据"""
    def __init__(self, receiver, localport, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.localport = localport
        self.remoteport = remoteport
        self.receiver = receiver    # 建立 Sender 与 Receiver 之间的联系
        receiver.sender = self      # 建立 Sender 与 Receiver 之间的联系
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建套接字
        self.connect((remoteaddr, remoteport))    # 连接远程主机

    def handle_connect(self):
        pass

    def handle_read(self):
        """接受来自远程主机的数据"""
        read = self.recv(BUFSIZE)
        self.receiver.from_remote_buffer += read
        print 'Sender read: ', self.receiver.from_remote_buffer

    def writable(self):
        """判断是否有来自本地请求要发送（如有则调用 handle_write）"""
        if len(self.receiver.to_remote_buffer) > 0:
            # 修改本地请求数据（将本地主机中 Host 改为远程主机地址）
            self.receiver.to_remote_buffer = self.receiver.to_remote_buffer.replace(LOCAL_SERVER_HOST + ':' + str(self.localport), REMOTE_SERVER_HOST + ':' + str(self.remoteport))
        return (len(self.receiver.to_remote_buffer) > 0)

    def handle_write(self):
        """发送本地请求数据"""
        sent = self.send(self.receiver.to_remote_buffer)
        self.receiver.to_remote_buffer = self.receiver.to_remote_buffer[sent:]
        print 'Sender write: ',  sent

    def handle_close(self):
        self.close()
        self.receiver.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stackless Socket Server Example')
    parser.add_argument('--local-host', action='store', dest='local_host', default=LOCAL_SERVER_HOST)
    parser.add_argument('--local-port', action='store', dest='local_port', type=int, required=True)
    parser.add_argument('--remote-host', action='store', dest='remote_host', default=REMOTE_SERVER_HOST)
    parser.add_argument('--remote-port', action='store', dest='remote_port', type=int, default=80)
    given_args = parser.parse_args()
    local_host, remote_host = given_args.local_host, given_args.remote_host
    local_port, remote_port = given_args.local_port, given_args.remote_port
    print "Starting port forwarding local %s:%s => remote %s:%s" % (local_host, local_port, remote_host, remote_port)
    PortForwarder(local_host, local_port, remote_host, remote_port)
    asyncore.loop()