#! /usr/bin/env python3

# Echo client program
import socket, sys, re


sys.path.append("../lib")       # for params
import params

from fileSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

FileName = input("Write file name:")
#FileName = 'Text.txt'
try:
    file = open(FileName,'r')

    #r = file.read().split('\n')
    r = file.read()
    r = r.replace('\n', '\0')           #It is not accepting the \n so I switch it to null which is \0 and still be aware of where is the next line
    file.close()

    #ch = '\0'


    #for i in r:
    #    print('RHERE', i)
    r = FileName+'//NAME//'+r           #I add this to send the name of the document attached to the file so we can put the same file name and I put this sign to show where I'll be separating this
    Newr = r.encode()                   #making the file in binary so I can send it


    print("sending",Newr)
    framedSend(s, Newr, debug)
    #r= file.read()
    print("received:", framedReceive(s, debug))
except FileNotFoundError:
    print("File Does Not Exist")





#print("sending hello world")
#framedSend(s, b"hello world", debug)
#print("received:", framedReceive(s, debug))

