# cliente.py
import socket
import time
import datetime

HOST = '127.0.0.1'  # O mesmo host do servidor
PORT = 65432        # A mesma porta do servidor

class RelogioLocal:
    """
    Simula um relógio local que pode estar dessincronizado
    e pode ser ajustado.
    """
    def __init__(self):
        # 'offset' é a diferença de tempo simulada do nosso relógio
        # para o relógio real do sistema.
        # Vamos simular que nosso relógio está 20 segundos adiantado.
        self._offset = 20.0  

    def get_tempo_local(self):
        """Retorna a hora "simulada" do nosso relógio local."""
        return time.time() + self._offset

    def ajustar_tempo(self, tempo_correto_estimado):
        """
        Ajusta o relógio. Na prática, recalculamos nosso offset
        em relação ao tempo real do sistema.
        """
        self._offset = tempo_correto_estimado - time.time()
        print(f"[Relógio Local] Tempo ajustado! Novo offset: {self._offset:+.4f}s")

    @staticmethod
    def formatar_timestamp(ts):
        """Função para formatar o tempo em formato legível com milissegundos."""
        # 
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def executar_sincronizacao(relogio):
    print("--- Iniciando Sincronização (Algoritmo de Christian) ---")
    print(f"Hora local (ANTES): {relogio.formatar_timestamp(relogio.get_tempo_local())}")

    try:
        # 1. Criar o socket e conectar ao servidor 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # 2. Registrar o tempo de envio (T_envio)
            # Usamos time.time() real, pois é a base para o RTT
            t_envio = time.time()

            # 3. Enviar uma solicitação (o conteúdo não importa)
            s.sendall(b'GET_TIME')

            # 4. Receber a resposta do servidor (hora do servidor)
            data = s.recv(1024)
            t_servidor = float(data.decode('utf-8'))
            
            # 5. Registrar o tempo de recebimento (T_recebimento)
            t_recebimento = time.time()

        # --- Início dos Cálculos ---
        
        # 6. Calcular o RTT (Round-Trip Time) 
        rtt = t_recebimento - t_envio
        
        # 7. Estimar o tempo de viagem de ida (metade do RTT) 
        tempo_viagem_ida = rtt / 2.0
        
        # 8. Calcular a hora correta estimada 
        # Hora correta = Hora do Servidor + Tempo de Viagem
        tempo_sincronizado = t_servidor + tempo_viagem_ida
        
        # 9. Ajustar o relógio local
        relogio.ajustar_tempo(tempo_sincronizado)
        
        # --- Exibição dos Resultados ---
        print("\n--- Resultados da Sincronização ---")
        print(f"Tempo do Servidor (Ts):   {relogio.formatar_timestamp(t_servidor)}")
        print(f"Tempo de Envio (T_envio): {relogio.formatar_timestamp(t_envio)}")
        print(f"Tempo de Receb. (T_receb):{relogio.formatar_timestamp(t_recebimento)}")
        print(f"RTT (T_receb - T_envio):  {rtt * 1000:.3f} ms") # 
        print(f"Tempo de Viagem (RTT/2):  {tempo_viagem_ida * 1000:.3f} ms")
        print("--------------------------------------------------")
        print(f"Hora Sincronizada (Ts + RTT/2): {relogio.formatar_timestamp(tempo_sincronizado)}")
        print(f"Hora local (DEPOIS):  {relogio.formatar_timestamp(relogio.get_tempo_local())}")

    except ConnectionRefusedError:
        print(f"Erro: Não foi possível conectar a {HOST}:{PORT}.")
        print("Verifique se o 'servidor.py' está em execução.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    meu_relogio_local = RelogioLocal()
    executar_sincronizacao(meu_relogio_local)