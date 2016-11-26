import socket
import threading
import SocketServer

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class ServerClient():
	def __init__(self, requestHandler):
		self.server = ThreadedTCPServer(("0.0.0.0", 7000), requestHandler)
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def start_server(self):
		self.server_thread.start()
	
	def connect_client(self,ip,port):
		self.sock.connect((ip, port))
	
	def send_message(self,message):
		try:
			self.sock.sendall(message)
		finally:
			self.sock.close()
	
	def stop_server(self):
		self.server.shutdown()
		self.server.server_close()

