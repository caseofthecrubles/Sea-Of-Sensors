#PYTHON SERVER TO HANDLE FEILD SENSORS
import socketserver
import socket
import logging
import logging.handlers
import threading
from datetime import datetime

# Set up the logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Set up the syslog handler
syslog_handler = logging.handlers.SysLogHandler(address=('log1.seantech.info', 514))
syslog_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(syslog_handler)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        try:
            # self.request is the TCP socket connected to the client
            self.request.settimeout(5)  # Set a timeout of 5 seconds
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            client_addr = ("{} wrote:".format(self.client_address[0]))
            print(self.data)
        
            #Push the data to syslog
            logger.info(str(self.data) + " " + str(self.server.server_address[1]) + " " + str(client_addr))
            # just send back the same data, but upper-cased
            self.request.sendall(self.data.upper())
        
            #Additional logging
            with open(f"socket_server_data{client_addr}.txt", "a") as sock_file:
                now = datetime.now()
                sock_file.write(str(now) + " " + str(self.data) + " " + str(self.server.server_address[1]) + " " + str(client_addr))
                sock_file.write("\n ")
        
            #Close the connection once complete/Close any damaged connections
            self.request.shutdown(socket.SHUT_RDWR)
            self.request.close()

        #Log the error encountered
        except Exception as e:
            logger.error(f"Error in connection: {e}")
            with open("socket_server.txt", "a") as sock_file:
                now = datetime.now()
                sock_file.write(str(now) + " " + "The socket failed or something MyTCPHandler")
                sock_file.write("\n ")

def create_and_run_server(host, port):
    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        print(f"Server running on port {port}")
        server.serve_forever()

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORTS = [1234, 1235, 1236]

    # Create the servers and run them on separate threads
    server_threads = []
    for port in PORTS:
        try:
            server_thread = threading.Thread(target=create_and_run_server, args=(HOST, port))
            server_thread.start()
            server_threads.append(server_thread)
        except:
            with open("socket_server.txt", "a") as sock_file:
                now = datetime.now()
                sock_file.write(str(now) + " " + "The socket failed or something main function " + str(port))
                sock_file.write("\n ")

    # Wait for all the threads to finish
    for server_thread in server_threads:
        server_thread.join()
