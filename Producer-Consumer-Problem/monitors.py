import threading
import time
import random

# Implementação do problema Produtor-Consumidor usando Monitores
class BufferMonitors:
    def __init__(self, size):
        self.buffer = []  # Lista que atuará como o buffer compartilhado
        self.size = size  # Tamanho máximo do buffer
        self.condition = threading.Condition()  # Condição para sincronização entre produtores e consumidores

    def produce(self, item):
        with self.condition:
            while len(self.buffer) >= self.size:  # Aguarda até que haja espaço no buffer
                self.condition.wait()
            self.buffer.append(item)  # Adiciona o item ao buffer
            print(f"(Monitors) Produtor produziu: {item}")
            self.condition.notify_all()  # Notifica que há um item disponível

    def consume(self):
        with self.condition:
            while len(self.buffer) == 0:  # Aguarda até que haja itens no buffer
                self.condition.wait()
            item = self.buffer.pop(0)  # Remove o item do buffer
            print(f"(Monitors) Consumidor consumiu: {item}")
            self.condition.notify_all()  # Notifica que há espaço disponível no buffer
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
    buffer = BufferMonitors(5)  # Inicializa o buffer com tamanho 5
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
