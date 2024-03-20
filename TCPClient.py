from socket import *

def block_selector(msg):
    blocks = [msg[i:i+8] for i in range(0,len(msg), 8)]
    blocks[-1] = blocks[-1].ljust(8)
    return blocks

def encrypt_message(msg, key):
    half = len(msg)//2
    left, right = msg[:half], msg[half:]
    new_right = "".join([right[int(k) - 1] for k in str(key)]) ^ left
    print(new_right)
    

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

#Conecta ao servidor
clientSocket.connect((serverName,serverPort))

#Recebe mensagem do usuario e envia ao servidor
message = input('Digite uma frase: ')
clientSocket.send(message.encode('ascii'))

encrypt_message(block_selector(message)[0],2314)

#Aguarda mensagem de retorno e a imprime
modifiedMessage, addr = clientSocket.recvfrom(2048)
print("Retorno do Servidor:",modifiedMessage.decode())

clientSocket.close()