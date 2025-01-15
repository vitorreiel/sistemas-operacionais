import threading
import time
import random

# Implementação com Monitores
class ReadersWritersMonitors:
    def __init__(self):
        self.read_count = 0  # Contador de leitores ativos
        self.condition = threading.Condition()  # Condição para sincronizar leitores e escritores

    def read(self, reader_id):
        with self.condition:
            self.read_count += 1
            if self.read_count == 1:
                self.condition.wait_for(lambda: self.read_count == 1)  # Bloqueia a escrita

        print(f"(Monitors) Leitor {reader_id} está lendo...")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"(Monitors) Leitor {reader_id} terminou de ler.")

        with self.condition:
            self.read_count -= 1
            if self.read_count == 0:
                self.condition.notify_all()  # Libera a escrita

    def write(self, writer_id):
        with self.condition:
            print(f"(Monitors) Escritor {writer_id} está escrevendo...")
            time.sleep(random.uniform(0.1, 0.5))
            print(f"(Monitors) Escritor {writer_id} terminou de escrever.")
            self.condition.notify_all()


# Funções dos leitores e escritores
def reader_task(rw, reader_id, num_reads):
    for _ in range(num_reads):
        rw.read(reader_id)
        time.sleep(random.uniform(0.1, 0.3))


def writer_task(rw, writer_id, num_writes):
    for _ in range(num_writes):
        rw.write(writer_id)
        time.sleep(random.uniform(0.1, 0.3))


# Função principal para rodar o teste e medir o tempo de execução
def run_readers_writers_test(buffer_class, num_readers=5, num_writers=2, num_operations=3):
    rw = buffer_class()

    threads = []

    # Cria threads para os leitores
    for i in range(num_readers):
        t = threading.Thread(target=reader_task, args=(rw, i + 1, num_operations))
        threads.append(t)

    # Cria threads para os escritores
    for i in range(num_writers):
        t = threading.Thread(target=writer_task, args=(rw, i + 1, num_operations))
        threads.append(t)

    start_time = time.time()  # Captura o tempo inicial

    # Inicia todas as threads
    for t in threads:
        t.start()

    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()

    end_time = time.time()  # Captura o tempo final
    print(f"Tempo total de execução: {end_time - start_time:.2f}s")  # Exibe o tempo total de execução


# Executa o teste com a implementação de monitores
run_readers_writers_test(ReadersWritersMonitors)
