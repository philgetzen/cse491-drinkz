#! /usr/bin/env python

import sys
import socket

def main(args):    
    address = args[1]    
    port = args[2]    
    GET = args[3]
    page = args[4]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s.connect((address, int(port)))    
    s.send("GET / HTTP/1.0\r\n\r\n")

    # Server takes GET and the destination following GET
    # Example: the following command
    s.send(GET + " " + page) # prints the Message Body of the HTTP Response
    
    while 1:        
	buf = s.recv(1000)        
	if not buf:            
	    break        
	print buf    

    print 'done'
    s.close()   

if __name__ == '__main__':   
   main(sys.argv)