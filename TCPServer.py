from socket import *

serverPort = 12000
#Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
#Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)

def block_selector(msg):
    blocks = [msg[i:i+8] for i in range(0,len(msg), 8)]
    return blocks

def xor(left, right, key):

    shuffled = shuffle(right, key)
    newleft = list(map(ord, list(right)))
    right = list(map(ord, list(shuffled)))
    left  = list(map(ord, list(left)))

    for i in range(0,len(left)):
        right[i] = right[i] ^ left[i]

    msg = newleft + right
    msg = "".join(list(map(chr, msg)))
    return msg

def shuffle(right, key):
    shuffled = list()
    for i in str(key):
      shuffled.append(right[int(i)-1])
    return shuffled

def decrypt_message(msg, key):
    half = len(msg)//2
    for i in range(4):
      left, right = msg[:half], msg[half:]
      msg = xor(left, right, key)
    
    left, right = msg[:half], msg[half:]
    msg = right + left
    return msg

def mapper(blocos, key):
    msg = ""
    for i in blocos:
      msg += decrypt_message(i, key)
    
    return msg

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")

key = 2314

while 1:
       #Cria um socket para tratar a conexao do cliente
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    print("{}".format(sentence.decode()))
    capitalizedSentence = sentence
    blocos = block_selector(capitalizedSentence.decode('ascii'))
    s = mapper(blocos, key)
    connectionSocket.send(s.encode('ascii').upper())
    connectionSocket.close()