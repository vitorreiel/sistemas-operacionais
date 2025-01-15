import threading
import time
import random

# Implementação do problema Produtor-Consumidor usando Semáforos
class BufferSemaphores:
    def __init__(self, size):
        self.buffer = []  # Lista que atuará como o buffer compartilhado
        self.size = size  # Tamanho máximo do buffer
        self.empty = threading.Semaphore(size)  # Semáforo que controla os espaços vazios no buffer
        self.full = threading.Semaphore(0)  # Semáforo que controla os itens disponíveis no buffer
        self.mutex = threading.Semaphore(1)  # Semáforo binário para garantir exclusão mútua

    def produce(self, item):
        self.empty.acquire()  # Aguarda até que haja espaço vazio no buffer
        self.mutex.acquire()  # Entra na seção crítica
        self.buffer.append(item)  # Adiciona o item ao buffer
        print(f"(Semaphores) Produtor produziu: {item}")
        self.mutex.release()  # Libera a seção crítica
        self.full.release()  # Sinaliza que há um item disponível no buffer

    def consume(self):
        self.full.acquire()  # Aguarda até que haja itens disponíveis no buffer
        self.mutex.acquire()  # Entra na seção crítica
        item = self.buffer.pop(0)  # Remove o item do buffer
        print(f"(Semaphores) Consumidor consumiu: {item}")
        self.mutex.release()  # Libera a seção crítica
        self.empty.release()  # Sinaliza que há espaço vazio disponível no buffer
        return item

# Funções do produtor e consumidor
def producer(buffer, total_items):
    for _ in range(total_items):
        item = random.randint(1, 100)  # Gera um item aleatório para produzir
        buffer.produce(item)
        time.sleep(random.uniform(0.01, 0.05))  # Aguarda antes de produzir novamente

def consumer(buffer, total_items):
    for _ in range(total_items):
        buffer.consume()  # Consome um item
        time.sleep(random.uniform(0.01, 0.05))  # Aguarda antes de consumir novamente

# Função principal para rodar o teste
def run_test(total_items):
    buffer = BufferSemaphores(5)  # Inicializa o buffer com tamanho 5
    start_time = time.time()  # Captura o tempo inicial

    # Cria as threads do produtor e consumidor
    producer_thread = threading.Thread(target=producer, args=(buffer, total_items))
    consumer_thread = threading.Thread(target=consumer, args=(buffer, total_items))

    # Inicia as threads
    producer_thread.start()
    consumer_thread.start()

    # Aguarda a conclusão das threads
    producer_thread.join()
    consumer_thread.join()

    end_time = time.time()  # Captura o tempo final
    print(f"Tempo total de execução: {end_time - start_time:.2f}s")

# Executa o teste
run_test(100)
