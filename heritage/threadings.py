import threading
import time

def tarefa(numero:int) -> None:
    print(f"Inicio da Tarefa {numero}")
    time.sleep(1)
    print(f"Fim da tarefa{numero}")

def main() -> None:
    threads = []
    for i in range(1,4):
        t= threading.Thread(target=tarefa,args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()