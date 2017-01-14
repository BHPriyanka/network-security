import sys,getopt
import thread
import socket,time

#initializing the default values of port and host
PORT= ' '
HOST = '0.0.0.0'

#an array to store the clients
clients = []
    
def main(argv):   

#Check the usage of the command
    if len(argv) < 2:
       print("Usage: ChatServer.py -p <portnumber>")
       sys.exit(2) 
    try:
       opts, args = getopt.getopt(argv,"p:")
    except getopt.GetoptError:
       sys.exit(2)

#Read the port number from command line       
    for opt, arg in opts:
       if opt == "-p":
          PORT = int(arg)

#Create a socket with UDP and INET
    try:

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print("Socket created")
    except socket.error:
        print("Failed to create socket. Error Code : ")
        sys.exit()

##Bind to the specified Host and Port
    try:
        s.bind((HOST,PORT))
    except socket.error:
        print("Bind failed. ")
        sys.exit()
	

#Start the thread message to receive messages from multiple clients
    thread.start_new_thread(receive_msg,(s,))
    try:
	while 1:
           pass
    except KeyboardInterrupt:
	print("Server closed")
	sys.exit(2)

def receive_msg(s):
    #for each message received from the client(one or more) do the following.
    while 1:
        try:
     
            d = s.recvfrom(1024)
            data = d[0]
            addr = d[1]

#if the client sends a GREETING message,record the client
            if data == "GREETING":
                clients.append(d)
                print("Accepted connection from : ")
		print(addr)
              
#If the message is anything else, broadcast it to all clients
    	    if data != "GREETING":
	
                #define the format of the message to be sent to the client
                inc = "INCOMING \n IP Address : " + addr[0] + "\n Port : " + str(addr[1]) + "\n " + data.strip()
		print("============================================================")
		print(inc)

		#for each client in the list create a thread
                for c in clients:
                    thread.start_new_thread(SendMsg,(s,c[1][0],c[1][1],inc))
                    time.sleep(5)	
        except socket.error:
        	print("BroadCast Error")
        	sys.exit(2)
        except:
            continue

#Function to send the message to the specified client
def SendMsg(socket,ip,port,msg):
     try:
	
        socket.sendto(msg, (ip, port))
     except:
          print("SendingFailed!")
          sys.exit(2)



##invoke the main method for execution   
if __name__ == "__main__":
    main(sys.argv[1:])



