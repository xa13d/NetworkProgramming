
import socket, json, os, sys, optparse


class Server:

    def __init__(self, port):
        self.interface = '127.0.0.1'
        self.port = port

    def listen(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.interface, self.port))
        s.listen(0)
        print("[LISTENING FOR CONNECTIONS]")
        self.connection, address = s.accept()
        print("[CONNECTED TO THE DEVICE:]" + str(address))

    def receiver(self):
    	json_data = ""
    	while True:
    		try:
    			json_data = json_data + self.connection.recv(1024).decode()
    			return json.loads(json_data)
    		except ValueError:
    			continue

    def send(self, data):
        jsn_data = json.dumps(data)
        self.connection.send(jsn_data.encode())


    def operate(self):
    	self.listen()
    	packet = self.receiver()
    	if (packet[0] == 'encode_decode'):
    		res = self.Encoder(packet[1], packet[2])
    	if (packet[0] == 'change_text'):
    		res = self.Changer(packet[1], packet[2])
    	self.send(res)

    def Changer(self, text, swaps):
    	tx = text.split()
    	dictio = eval(swaps)
    	for word in tx:
    		if word in dictio.keys():
    			text = text.replace(word, dictio[word])
    	return text


    def Encoder(self, text, key):
    	enc = ""
    	for i in range(len(text)):
    		char = text[i]
    		k = key[i%len(key)]
    		enc += chr(ord(char) ^ ord(k))
    	return enc




class Client:

	def __init__(self, mode):
		self.mode = mode


	def connect(self, interface, port):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((interface, port))


	def send(self, data):
		jn_data = json.dumps(data)
		self.connection.send(jn_data.encode())


	def receiver(self):
		jn_data = ""
		while True:
			try:
				jn_data = jn_data + self.connection.recv(1024).decode()
				return json.loads(jn_data)
			except ValueError:
				continue


	def processor(self, f, a):
		msg = open(f, 'r').read()
		aux = open(a, 'r').read()
		data = []
		data.append(self.mode)
		data.append(msg)
		data.append(aux)
		self.send(data)
		packet = self.receiver()
		print(packet)



def main():
	parser = optparse.OptionParser()
	parser.add_option("-p", metavar="PORT", type= int, help="Listening Port")
	if sys.argv[1] == "client":
		parser.add_option("--host", dest = "interface", help="Destination IP Address")
		parser.add_option("-m", dest = "mode", help="Operating Mode")
		parser.add_option("-f", dest = "f", help="File")
		parser.add_option("-a", dest = "a", help="[JSON/KEY]")
	(options,arguments) = parser.parse_args()
	if sys.argv[1] == "client":
		client = Client(options.mode)
		client.connect(options.interface, options.p)
		client.processor(options.f, options.a)
	else:
		server = Server(options.p)
		server.operate()

if __name__== "__main__":
	main()