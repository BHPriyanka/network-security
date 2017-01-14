#Client-Server Broadcast Chat Application
The files server.py and client.py are the files for the server and the client, respectively. <br />

The server program takes only the port number in command line without any option and the client program takes the hostname and the port number on command line.  <br />
No options are configured like -sp,etc. <br />

The code is not implemented using threads. This code works in Linux environment. I have tested it on Linux VM <br />

sample running of the server program: <br />

Give the port number for the server to bind. <br />
team@nslabu:~/bhpr$ python server.py 9999 <br />
Socket created <br />
Socket Bind complete <br />
Server Initialized... <br />


Sample running of the client program: <br />
Give the hostname and the same port number as given for the server program. <br />

team@nslabu:~/bhpr$ python client.py <br />
Usage : python telnet.py hostname port <br />
team@nslabu:~/bhpr$ python client.py 127.0.0.1 9999 <br />
<You> <br />
 <br />
 Now on the server window: <br />
team@nslabu:~/bhpr$ python server.py 9999 <br />
Socket created <br />
Socket Bind complete <br />
Server Initialized... <br />
Accepted connection from :  127.0.0.1 <br />
 <br />
Message[127.0.0.1:41955] -GREETING <br />
 <br />
On the client window: <br />
 <br />
team@nslabu:~/bhpr$ python client.py 127.0.0.1 9999 <br />
<You> Hi <br />
Server reply : <br />
INCOMING <br />
 IP Address : 127.0.0.1 <br />
 Port : 41955 <br />
 Message: Hi <br />
 <br />
 <br />
Server window: <br />
team@nslabu:~/bhpr$ python server.py 9999 <br />
Socket created <br />
Socket Bind complete <br />
Server Initialized... <br />
Accepted connection from :  127.0.0.1 <br />
 <br />
Message[127.0.0.1:41955] -GREETING <br />
Accepted connection from :  127.0.0.1 <br />
 <br />
Message[127.0.0.1:41955] -Hi <br />
 <br />
and then, when the new client pings, the broadcast happens. <br />

