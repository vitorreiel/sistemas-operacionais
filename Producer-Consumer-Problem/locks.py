import threading
import time
import random

# Implementação do problema Produtor-Consumidor usando Locks e Mutexes
class BufferLocks:
    def __init__(self, size):
        self.buffer = []  # Lista que atuará como o buffer compartilhado
        self.size = size  # Tamanho máximo do buffer
        self.lock = threading.Lock()  # Lock para exclusão mútua
        self.not_full = threading.Condition(self.lock)  # Condição para buffer não cheio
        self.not_empty = threading.Condition(self.lock)  # Condição para buffer não vazio

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.size:  # Aguarda até que haja espaço no buffer
                self.not_full.wait()
            self.buffer.append(item)  # Adiciona o item ao buffer
            print(f"(Locks/Mutexes) Produtor produziu: {item}")
            self.not_empty.notify()  # Notifica que há um item disponível

    def consume(self):
        with self.not_empty:
            while len(self.buffer) == 0:  # Aguarda até que haja itens no buffer
                self.not_empty.wait()
            item = self.buffer.pop(0)  # Remove o item do buffer
            print(f"(Locks/Mutexes) Consumidor consumiu: {item}")
            self.not_full.notify()  # Notifica que há espaço disponível no buffer
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
    buffer = BufferLocks(5)  # Inicializa o buffer com tamanho 5
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
