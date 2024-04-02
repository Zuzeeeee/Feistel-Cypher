from socket import *

def block_selector(msg):
    blocks = [msg[i:i+8] for i in range(0,len(msg), 8)]
    blocks[-1] = blocks[-1].ljust(8)
    return blocks

def encrypt_message(msg, key):
    half = len(msg)//2
    for i in range(4):
        left, right = msg[:half], msg[half:]
        msg = xor(left, right, key)

    left, right = msg[:half], msg[half:]
    msg = right + left
    return msg

def shuffle(right, key):
    shuffled = list()
    for i in str(key):
        shuffled.append(right[int(i)-1]) 
    return shuffled

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

def mapper(blocos):
    lista = []
    for i in blocos:
        lista.append(encrypt_message(i, key).encode('ascii'))
    msg = b''.join(lista)
    return msg

    
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
key = 2314

#Conecta ao servidor
clientSocket.connect((serverName,serverPort))

#Recebe mensagem do usuario e envia ao servidor
message = input('Digite uma frase: ')

lista = block_selector(message)

msg = mapper(lista)

encrypted = encrypt_message(block_selector(message)[0], key)
clientSocket.send(msg)

#Aguarda mensagem de retorno e a imprime
modifiedMessage, addr = clientSocket.recvfrom(2048)
print("Retorno do Servidor:",modifiedMessage.decode())

clientSocket.close()