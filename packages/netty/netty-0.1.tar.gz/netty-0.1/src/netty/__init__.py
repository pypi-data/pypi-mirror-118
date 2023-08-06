from netty import connection
from netty import examples
import pickle
import socket

def encode(obj):
    o = pickle.dumps(obj)
    length = str(len(o)).encode().rjust(4, b'0')
    return length + o

def getMyIp():
    return(str(socket.gethostbyname(socket.gethostname())))

def getMyPublicIp():
    return(str(socket.gethostbyname('localhost')))
