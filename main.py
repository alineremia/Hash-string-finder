import socket
import ssl
import random
import string
import hashlib
import datetime
import time
from string import ascii_lowercase
import binascii
from base64 import b64encode
from random import random


#   18.202.148.130 "srv.exatest.dynu.net"
#   3335, 8082, 8445, 49154, 3480, 65533
HOST = "some.server.net"
PORT = 8080
authdata = "authdata"
the_time = datetime.datetime.now()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(certfile="bundle.pem", keyfile="bundle.pem")
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("bundle.pem")
conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
 
d1 = datetime.datetime.now()
print("Start timestamp" + str(d1))


def randomString(stringLength=10):
    lis = list(ascii_lowercase)
    return "".join( [lis[int(random() * 26)] for _ in range(stringLength)] )  
    #return ''.join(random.choice(string.ascii_lowercase) for i in range(stringLength))

def multiplyZeros(number):
    zero_str = ""
    for x in range(int(number)):
        zero_str = zero_str + "0"
    return zero_str

def computesha(difficulty, authdata, suffix):
    Nonce = 0
    while 1:
        hash = authdata+suffix+str(Nonce)
        newHash = hashlib.sha1(hash.encode()).hexdigest()
        if newHash[:6] == '000000':
            return hash, suffix, Nonce
            break
        else :          
            Nonce += 1



conn.connect((HOST, PORT))
args = conn.recv().decode('utf-8').strip().split(' ') 
print(args[0])

if args[0] == "HELLO":
    conn.send("HELLO\n".encode('utf-8'))
    args = conn.recv().decode('utf-8').strip().split(' ')
    print(args)
elif args[0] == "ERROR":
    print("ERROR: " + " ".join(args[1:]))
    #break
if args[0] == "MESSAGE":
    authdata, difficulty = args[1], args[2]
   
    while 1:
     
        print(authdata)

     

        suffix = randomString()
        test = computesha("000000", authdata, suffix)
        print(test)
        print(authdata)
        d2 = datetime.datetime.now()                 
        print("End timestamp " + str(d2))
        print("Elapsed time: " + str((d2-d1)))
      
        cksum_in_hex = test[0]
        suffix_in_func = test[2]
        suffix_count = test[1]
        suffix_to_send = str(suffix_in_func) + str(suffix_count)
        check_obj = str(cksum_in_hex).strip()
        checksum_bool = check_obj.startswith("000000")
    
        print(cksum_in_hex)
        print(suffix_to_send)
        print(checksum_bool)
        print(the_time)
        #break
        # check if the checksum has enough leading zeros
        # (length of leading zeros should be equal to the difficulty)
        if checksum_bool:
            conn.send((suffix_to_send + "\n").encode('utf-8'))
            args = conn.recv().decode('utf-8') # ERROR wrong POW data why?
			if args[0] == "END":
			conn.write("END\n")         
            break
			elif args[0] == "ERROR":
			print("ERROR: " + " ".join(args[1:]))

conn.shutdown(socket.SHUT_RDWR)
conn.close()
