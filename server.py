import socket
import datetime

# configs do server
ip = '127.0.0.1'
port = 12345
buffer = 1024
# variável pra armazenar os clientes conectados
clients = {}
# criação do socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((ip, port))
print(f"Server UDP rodando em {ip}:{port}")

received_data = {}  # armazenamento de temps

def broadcast(message, sender_address):
    # fragmenta a mensagem antes de enviar
    for client_address in clients:
        if client_address != sender_address:
            send_file(client_address, message.encode())

def send_file(address, data):
    try:
        total_size = len(data)
        for i in range(0, total_size, buffer):
            chunk = data[i:i + buffer]
            server.sendto(chunk, address)
        # envia um pacote vazio para indicar o fim da transmissão
        server.sendto(b'', address)
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def process_msg(data, address):
    try:
        if address not in received_data:
            received_data[address] = []
        received_data[address].append(data)

        # verifica se a transmissão foi concluída
        if data == b'':
            full_message = b''.join(received_data[address][:-1]).decode('utf-8', errors='replace')
            del received_data[address]

            if address not in clients:
                # para capturar o username da mensagem inicial
                parts = full_message.split()
                if len(parts) > 3 and parts[0] == "hi," and parts[1] == "meu" and parts[2] == "nome" and parts[3] == "eh":
                    username = " ".join(parts[4:])
                    clients[address] = username
                    broadcast(f"{username} entrou na sala.", address)
                    print(f"{username} ({address[0]}:{address[1]}) conectou-se à sala.")
                else:
                    print("Mensagem de conexão inválida recebida.")
            else:
                username = clients[address]
                timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                formatted_message = f"{address[0]}:{address[1]}/~{username}: {full_message} {timestamp}"
                broadcast(formatted_message, address)
                print(formatted_message)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def receive():
    while True:
        data, address = server.recvfrom(buffer)
        process_msg(data, address)

if __name__ == "__main__":
    receive()
