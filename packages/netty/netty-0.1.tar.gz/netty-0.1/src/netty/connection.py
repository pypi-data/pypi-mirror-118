from netty import crypttools as crypt
import socket, threading, pickle, json, sys
from netty import handle
import time
import netty

class ErrorDisconnectedFromServer(Exception):
    pass

class ErrorReceivingMessage(Exception):
    pass

class ErrorSendingMessage(Exception):
    pass

class ErrorMessageNotFromServer(Exception):
    pass

class ErrorConnectingToServer(Exception):
    pass

__HEADER_SIZE__ = 4
__HEADER_AMOUNT__ = 4

class Client:
  def __init__(self, ip, port, onReceive=lambda x: None):
    self.ip = ip
    
    self.port = port
    
    self.uid = crypt.strHash(str(self.ip) + '$@lt' + str(self.port))
    
    self.connected = False
    
    self.connection = None
    self.onReceive = onReceive
    self.timeLast = time.time()
  
  def _dict_wrapper(self, data, type_='data'):
        return {
            'uid': self.uid,
            'time': time.time(),
            'payload': data,
            'type': type_
        }
    
  def _receive_once(self):
    #print('recv')
    try: received = self.connection.recv(__HEADER_SIZE__)
    except: pass
    if received == b'': return
    try:
        received = int(received)
    except:
        print("Recv amount ==>> int -- failed")
        pass
    mes = None
    try:
        data = self.connection.recv(received)
        mes = pickle.loads(data)
        mes = handle.Message(mes)
    except:
        pass
    try:
        if mes != None:
            self.onReceive(mes)
    
    except:
        print("Closing...")
        self.connection.close()
        raise ErrorDisconnectedFromServer

  def _rec_forever(self):
      while True:
          self._receive_once()
          
  def connect(self):
    assert not self.connected
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.connection.connect((str(self.ip), int(self.port)))
      self.connected = True
    except:
      self.connected = False
      self.connection = None
      raise ErrorConnectingToServer

  def send(self, data):
    #print(data)
    
    assert self.connected
    wrapper = self._dict_wrapper(data)
    dumped_wrapper = pickle.dumps(wrapper)
    try:            
        self.connection.sendall(str(len(dumped_wrapper)).encode().rjust(4, b'0'))
        self.connection.sendall(dumped_wrapper)
        #print('sent mes successfully!')
    except:
        raise ErrorSendingMessage

  def start(self):
      try:
          assert not self.connected
          self.connect()
          thread = threading.Thread(target=self._rec_forever)
          thread.start()
          print('Successfully started!')
      except:
          print('Failed to connect to server! Try again!')
          raise ErrorConnectingToServer

        

class Server:
    def __init__(self, port, onReceive=lambda x, y: None, _newthread_client=True):
        self.port = port
        self.ip = ''
        self.started = False
        self._clients = []
        self._clientthreads = []
        self.clients = []
        self.onReceive = onReceive
        self._newthread_client = _newthread_client
        
    def _handle_single(self, client):
        while True:
            numchars = client.recv(__HEADER_AMOUNT__)
            if numchars == b'':
                continue
            numchars = int(numchars)
            data = client.recv(numchars)
            if not data == b'':
                data = pickle.loads(data)
                self.onReceive(data, self._clients)
            

    def _handle_all(self):
        for c in self._clients:
            try:
                things = c.recv(__HEADER_AMOUNT__)
                if things == b'':
                    continue
                chars = int(things)
                data = c.recv(chars)
                #print("Number of characters:", chars)
                if not data == b'':
                    data = pickle.loads(data)
                    self.onReceive(data, self._clients)
                else:
                    c.close()
                    print('Removing client: ' + str(c) + "\n   -Reason: Not online or not reachable")
                    self._clients.remove(c)
            except:
                c.close()
                print('Removing client: ' + str(c) + "\n   -Reason: Not online or not reachable")
                self._clients.remove(c)
    def _handle_forever(self):
        while True:
            self._handle_all()

    def _accept_once(self):
        client, address = self.listener.accept()
        self._clients.append(client)
        print("Got client: %s" % client)
    def _accept_forever(self):
        while True:
            self._accept_once()
    def _accept_newthread_forever(self):
        while True:
            print("Newthread -- accepting")
            client, address = self.listener.accept()
            self._clients.append(client)
            point = len(self._clientthreads)
            print("Got client:", client)
            self._clientthreads.append(threading.Thread(target=self._handle_single, args = (client, )))
            self._clientthreads[point].start()

    def start(self):
        assert not self.started
        print("Starting server")
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.ip, self.port))
        self.listener.listen(2)
        if not self._newthread_client:
            self.acceptThread = threading.Thread(target=self._accept_forever)
            self.acceptThread.start()
            self.handleThread = threading.Thread(target=self._handle_forever)
            self.handleThread.start()
        else:
            self.acceptThread = threading.Thread(target=self._accept_newthread_forever)
            self.acceptThread.start()
        ip = self.ip
        if str(ip) == "":
            ip = netty.getMyIp()
        elif str(ip) == "-p":
            ip = netty.getMyPublicIp()
        print('Server successfully started!\n\t-Ip: "' + str(ip) + '"\n\t-Port: "' + str(self.port) + '"')             
            
            
        
        
    
