
import sys,getopt
import thread,socket,time

#Set the values of port and host to void
port=' '
host = ' '

def main(argv):
    
##Check if there are enough command line arguments,if not prompt the user to enter all the arguments    
    if len(argv) < 2:
       print("Usage: ChatClient.py -s <Server_IPaddress> -p <portnumber>")
       sys.exit(2) 


#Assign the user input of Port and Host to the variables
    try:
       opts, args = getopt.getopt(argv,"s:p:")
    except getopt.GetoptError:
       sys.exit(2)
       
    for opt, arg in opts:
       if opt == "-p":
          port = arg
       elif opt =="-s":
           host = arg

    
#Open the socket with UDP protocol type.handle the exception if it fails by displaying appropriate error code
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit()

#Bind the client to the specified host and with port number as 0.Since there will be multiple clients,the server will allocate the port numbers randomly to the clients
    try:
           s.bind((host,0))
    except socket.error:
           print("Bind failed. Error Code: ")
           sys.exit()

#Send the GREETING message to the server indicating its first encounter with the server
    msg = b'GREETING'
    s.sendto(msg,(host, int(port)))

#start the threads to send and receive messages to and from the server
    thread.start_new_thread(receive,(s,))
    thread.start_new_thread(SendMsg,(s,host,port))

    while 1:
        pass


#function to receive message from the server
def receive(s):
    while 1:
        try:
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
	    print("=====================================================")
	    print(reply) 
	    print("=====================================================")

            #if reply == 'INCOMING':
                #print(reply)
            time.sleep(5)
        except socket.error:
            print("BroadCast error")
            sys.exit(2)
        except:
            continue

#function to send message to the server
def SendMsg(c,ip,port):
    while 1:
	
	MESSAGE="MESSAGE: " + raw_input()
        try:
            c.sendto(MESSAGE,(ip,int(port)))
        except socket.error:
            print("Send Error")
            sys.exit(2)
        time.sleep(5)


if __name__ == "__main__":
   main(sys.argv[1:])
