import threading
import time
import random
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd

# Criação das pastas para armazenar gráficos e dataset
if not os.path.exists("graficos"):
    os.makedirs("graficos")
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Implementação com Semáforos
class ReadersWritersSemaphores:
    def __init__(self):
        self.read_count = 0  # Contador de leitores ativos
        self.mutex = threading.Semaphore(1)  # Controle de acesso ao contador de leitores
        self.write_lock = threading.Semaphore(1)  # Controle de acesso exclusivo para escritores

    def read(self, reader_id):
        # Controle de entrada de leitores
        self.mutex.acquire()
        self.read_count += 1
        if self.read_count == 1:  # Se for o primeiro leitor, bloqueia os escritores
            self.write_lock.acquire()
        self.mutex.release()

        # Simula a leitura
        print(f"(Semáforos) Leitor {reader_id} está lendo...")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"(Semáforos) Leitor {reader_id} terminou de ler.")

        # Controle de saída de leitores
        self.mutex.acquire()
        self.read_count -= 1
        if self.read_count == 0:  # Se não houver mais leitores, libera os escritores
            self.write_lock.release()
        self.mutex.release()

    def write(self, writer_id):
        # Controle de exclusão mútua para escritores
        self.write_lock.acquire()
        print(f"(Semáforos) Escritor {writer_id} está escrevendo...")
        time.sleep(random.uniform(0.1, 0.5))  # Simula a escrita
        print(f"(Semáforos) Escritor {writer_id} terminou de escrever.")
        self.write_lock.release()

# Implementação com Monitores
class ReadersWritersMonitors:
    def __init__(self):
        self.read_count = 0  # Contador de leitores ativos
        self.condition = threading.Condition()  # Condição para sincronização entre leitores e escritores

    def read(self, reader_id):
        # Controle de entrada de leitores
        with self.condition:
            self.read_count += 1
            if self.read_count == 1:  # Se for o primeiro leitor, espera que escritores terminem
                self.condition.wait()

        # Simula a leitura
        print(f"(Monitores) Leitor {reader_id} está lendo...")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"(Monitores) Leitor {reader_id} terminou de ler.")

        # Controle de saída de leitores
        with self.condition:
            self.read_count -= 1
            if self.read_count == 0:  # Se não houver mais leitores, notifica todos
                self.condition.notify_all()

    def write(self, writer_id):
        # Controle de exclusão mútua para escritores
        with self.condition:
            print(f"(Monitores) Escritor {writer_id} está escrevendo...")
            time.sleep(random.uniform(0.1, 0.5))  # Simula a escrita
            print(f"(Monitores) Escritor {writer_id} terminou de escrever.")
            self.condition.notify_all()  # Notifica leitores que a escrita terminou

# Implementação com Locks/Mutexes
class ReadersWritersLocks:
    def __init__(self):
        self.read_count = 0  # Contador de leitores ativos
        self.lock = threading.Lock()  # Controle de acesso ao contador de leitores
        self.write_lock = threading.Lock()  # Controle de acesso exclusivo para escritores

    def read(self, reader_id):
        # Controle de entrada de leitores
        with self.lock:
            self.read_count += 1
            if self.read_count == 1:  # Se for o primeiro leitor, bloqueia os escritores
                self.write_lock.acquire()

        # Simula a leitura
        print(f"(Locks/Mutexes) Leitor {reader_id} está lendo...")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"(Locks/Mutexes) Leitor {reader_id} terminou de ler.")

        # Controle de saída de leitores
        with self.lock:
            self.read_count -= 1
            if self.read_count == 0:  # Se não houver mais leitores, libera os escritores
                self.write_lock.release()

    def write(self, writer_id):
        # Controle de exclusão mútua para escritores
        with self.write_lock:
            print(f"(Locks/Mutexes) Escritor {writer_id} está escrevendo...")
            time.sleep(random.uniform(0.1, 0.5))  # Simula a escrita
            print(f"(Locks/Mutexes) Escritor {writer_id} terminou de escrever.")

# Funções dos leitores e escritores
def reader_task(rw, reader_id, num_reads):
    for _ in range(num_reads):  # Cada leitor executa múltiplas leituras
        rw.read(reader_id)

def writer_task(rw, writer_id, num_writes):
    for _ in range(num_writes):  # Cada escritor executa múltiplas escritas
        rw.write(writer_id)

# Função principal para rodar o teste e medir o tempo de execução
def run_readers_writers_test(buffer_class, num_readers=5, num_writers=2, num_operations=3):
    rw = buffer_class()  # Inicializa a classe do buffer
    threads = []  # Lista para armazenar as threads

    # Cria threads para leitores
    for i in range(num_readers):
        t = threading.Thread(target=reader_task, args=(rw, i + 1, num_operations))
        threads.append(t)

    # Cria threads para escritores
    for i in range(num_writers):
        t = threading.Thread(target=writer_task, args=(rw, i + 1, num_operations))
        threads.append(t)

    start_time = time.time()

    # Inicia todas as threads
    for t in threads:
        t.start()

    # Aguarda a finalização de todas as threads
    for t in threads:
        t.join()

    end_time = time.time()
    return end_time - start_time

# Pergunta ao usuário o número de repetições
num_repeticoes = int(input("Quantas vezes esses testes serão repetidos? "))

# Salva os tempos de execução em um dataset
csv_path = "dataset/dataset.csv"
with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Execução", "Semáforos", "Monitores", "Locks/Mutexes"])

    for repeticao in range(1, num_repeticoes + 1):
        print(f"\nIniciando repetição {repeticao}/{num_repeticoes}...")

        # Executa os testes para cada abordagem
        tempos = {
            "Semáforos": run_readers_writers_test(ReadersWritersSemaphores),
            "Monitores": run_readers_writers_test(ReadersWritersMonitors),
            "Locks/Mutexes": run_readers_writers_test(ReadersWritersLocks)
        }

        writer.writerow([repeticao, tempos["Semáforos"], tempos["Monitores"], tempos["Locks/Mutexes"]])

# Gera o gráfico com base nos dados
# Lê os dados do dataset
data = pd.read_csv(csv_path)
media_tempos = data["Semáforos", "Monitores", "Locks/Mutexes"].mean()

grafico_path = "graficos/comparison_average.png"
plt.figure(figsize=(10, 6))
plt.bar(media_tempos.index, media_tempos.values, color=['blue', 'green', 'orange'])

for i, value in enumerate(media_tempos.values):
    plt.text(i, value + 0.05, f"{value:.2f}s", ha='center', va='bottom')

plt.xlabel("Mecanismo de Exclusão Mútua")
plt.ylabel("Tempo Médio de Execução (s)")
plt.title("Comparação de Tempos Médios - Leitores e Escritores")
plt.grid(axis='y')
plt.savefig(grafico_path)