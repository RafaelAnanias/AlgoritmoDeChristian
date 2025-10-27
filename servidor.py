# servidor.py
import socket
import time

HOST = '127.0.0.1'  # Endereço IP do servidor (localhost)
PORT = 65432        # Porta para ouvir

def iniciar_servidor():
    # 1. Criar um socket TCP/IP 
    # AF_INET = família de endereços IPv4
    # SOCK_STREAM = protocolo TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # 2. Vincular o socket ao endereço e porta
        s.bind((HOST, PORT))
        
        # 3. Começar a ouvir por conexões
        s.listen()
        
        print(f"Servidor de tempo ouvindo em {HOST}:{PORT}...")
        
        # 4. Loop infinito para aceitar conexões
        while True:
            # Aceita uma nova conexão (bloqueante)
            conn, addr = s.accept()
            with conn:
                print(f"Conexão recebida de {addr}")
                
                # 5. Obter a hora atual do servidor (em segundos, com milissegundos)
                tempo_servidor = time.time()
                
                # 6. Enviar a hora como string codificada em bytes 
                conn.sendall(str(tempo_servidor).encode('utf-8'))
                
                # A conexão é fechada automaticamente ao sair do 'with conn'

if __name__ == "__main__":
    iniciar_servidor()