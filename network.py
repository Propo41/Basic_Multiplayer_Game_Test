import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.108"
        self.port = 5555
        self.address = (self.server, self.port)
        self.pos = self.connect()
        print("received from server: ", self.pos)

    # used only once during creation of this class
    # used to fetch initial values from the server
    def connect(self):
        try:
            self.client.connect(self.address)  # connect the client to the server using the address provided
            print("connected to server")
            return self.client.recv(2048).decode()  # receive whatever msg is sent from server and decode

        except:
            print("connection couldn't be established from client side")

    # used more than once to send and receive data continuously
    # sends the given data as a parameter to the server and receives back whatever is send from it
    def send(self, data):
        try:
            print("sending to server: ", data)
            self.client.send(str.encode(data))  # send data given as a parameter to the server
            received = self.client.recv(2048).decode()  # receive whatever msg is sent from server and decode
            print("received from server: ", received)
            return received
        except socket.error as e:
            print(e)

    def get_pos(self):
        return self.pos



#test_network = Network()
#test_network.send("hello")
