import threading
import time
import random
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd

# Certifique-se de que as pastas necessárias existem
if not os.path.exists("dataset"):
    os.makedirs("dataset")
if not os.path.exists("graficos"):
    os.makedirs("graficos")

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

# Implementação do problema Produtor-Consumidor usando Monitores
class BufferMonitors:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.condition = threading.Condition()

    def produce(self, item):
        with self.condition:
            while len(self.buffer) >= self.size:
                self.condition.wait()
            self.buffer.append(item)
            print(f"(Monitors) Produtor produziu: {item}")
            self.condition.notify_all()

    def consume(self):
        with self.condition:
            while len(self.buffer) == 0:
                self.condition.wait()
            item = self.buffer.pop(0)
            print(f"(Monitors) Consumidor consumiu: {item}")
            self.condition.notify_all()
            return item

# Implementação do problema Produtor-Consumidor usando Semáforos
class BufferSemaphores:
    def __init__(self, size):
        self.buffer = []  # Lista que atuará como o buffer compartilhado
        self.size = size  # Tamanho máximo do buffer
        self.empty = threading.Semaphore(size)  # Contador de espaços vazios no buffer
        self.full = threading.Semaphore(0)  # Contador de itens disponíveis no buffer
        self.mutex = threading.Semaphore(1)  # Semáforo binário para exclusão mútua

    def produce(self, item):
        self.empty.acquire()  # Decrementa o semáforo de espaços vazios
        self.mutex.acquire()  # Garante exclusão mútua
        self.buffer.append(item)  # Adiciona o item ao buffer
        print(f"(Semaphores) Produtor produziu: {item}")
        self.mutex.release()  # Libera o semáforo binário
        self.full.release()  # Incrementa o semáforo de itens disponíveis

    def consume(self):
        self.full.acquire()  # Decrementa o semáforo de itens disponíveis
        self.mutex.acquire()  # Garante exclusão mútua
        item = self.buffer.pop(0)  # Remove o primeiro item do buffer
        print(f"(Semaphores) Consumidor consumiu: {item}")
        self.mutex.release()  # Libera o semáforo binário
        self.empty.release()  # Incrementa o semáforo de espaços vazios
        return item

# Funções do produtor e consumidor
def producer(buffer, total_items):
    for _ in range(total_items):
        item = random.randint(1, 100)  # Gera um número aleatório
        buffer.produce(item)  # Adiciona o item ao buffer
        time.sleep(random.uniform(0.01, 0.05))  # Simula atraso na produção

def consumer(buffer, total_items):
    for _ in range(total_items):
        buffer.consume()  # Remove um item do buffer
        time.sleep(random.uniform(0.01, 0.05))  # Simula atraso no consumo

# Função para medir o tempo de execução de um teste
def measure_time(buffer_class, total_items):
    buffer = buffer_class(5)  # Cria uma instância do buffer com tamanho 5
    start_time = time.time()

    # Cria as threads para o produtor e consumidor
    producer_thread = threading.Thread(target=producer, args=(buffer, total_items))
    consumer_thread = threading.Thread(target=consumer, args=(buffer, total_items))

    # Inicia as threads
    producer_thread.start()
    consumer_thread.start()

    # Aguarda a finalização das threads
    producer_thread.join()
    consumer_thread.join()

    end_time = time.time()
    return end_time - start_time

# Pergunta ao usuário quantas vezes os testes devem ser repetidos
repeat_count = int(input("Quantas vezes esses testes serão repetidos? "))

dataset_path = "dataset/dataset.csv"

# Criação do arquivo CSV para armazenar os resultados
with open(dataset_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Execução", "Semáforos", "Monitores", "Locks/Mutexes"])

    for i in range(1, repeat_count + 1):
        print(f"Iniciando execução {i} de {repeat_count}...")
        tempos = {
            "Semáforos": measure_time(BufferSemaphores, 100),
            "Monitores": measure_time(BufferMonitors, 100),
            "Locks/Mutexes": measure_time(BufferLocks, 100),
        }
        writer.writerow([i, tempos["Semáforos"], tempos["Monitores"], tempos["Locks/Mutexes"]])

# Geração do gráfico comparativo com base nos resultados
data = pd.read_csv(dataset_path)
avg_times = data.mean().iloc[1:]

plt.bar(avg_times.index, avg_times.values, color=['blue', 'green', 'orange'])
plt.ylim(0, max(avg_times.values) * 1.2)
for i, value in enumerate(avg_times.values):
    plt.text(i, value + 0.05, f"{value:.2f}s", ha='center', va='bottom')
plt.xlabel('Mecanismo de Exclusão Mútua')
plt.ylabel('Tempo Médio de Execução (s)')
plt.title('Comparação Média de Tempos de Execução - Produtor-Consumidor')
plt.savefig("graficos/comparison_average.png")
