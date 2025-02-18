import socket
import threading
import os

# configs do cliente
ip = '127.0.0.1'
port = 12345
buffer = 1024
# criação de um socket UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(buffer)
                if not data:
                    break
                client.sendto(data, (ip, port))
            # envia um pacote vazio para indicar o fim da transmissão
            client.sendto(b'', (ip, port))
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def send(message):
    try:
        temp_file = "temp_message.txt"
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(message)
        send_file(temp_file)
        os.remove(temp_file)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

received_data = {}  # armazenamento de temps

def receive():
    while True:
        try:
            msg_recebida, address = client.recvfrom(buffer)
            if address not in received_data:
                received_data[address] = []
            received_data[address].append(msg_recebida)

            # verifica se a transmissão foi concluída
            if msg_recebida == b'':
                full_message = b''.join(received_data[address][:-1]).decode('utf-8', errors='ignore')
                print(f"\nMensagem recebida:\n{full_message}")
                del received_data[address]
        except ConnectionResetError:
            print("Conexão caiu!")
            break
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            continue

# starta o chat
def start_chat():
    username = input("Digite seu username: ")
    send(f"hi, meu nome eh {username}")
    # thread para receber mensagens
    threading.Thread(target=receive, daemon=True).start()
    # loop principal
    while True:
        message = input()
        if message.lower() == 'bye':
            send("bye")
            break
        send(message)

if __name__ == "__main__":
    start_chat()
