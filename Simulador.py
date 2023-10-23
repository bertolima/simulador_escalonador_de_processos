from Processo import Processo
import time
from collections import deque

class Simulador:
    def __init__(self, quantum = None, sobrecarga = None):
        self.quantum = quantum
        self.sobrecarga = sobrecarga
        self.processos:deque[Processo] = deque()
        self.ended = []
        self.turnaround = 0
        self.time = 0
    
    def criarProcesso(self, tempoChegada:int, tempoExec:int, deadline:int, prioridade:int, paginas:int):
        self.processos.append(Processo(tempoChegada, tempoExec, deadline, prioridade, paginas))
    
    def restart(self):
        for elem in reversed(self.ended):
            elem.restart()
            self.processos.append(elem)
        
        self.ended.clear()
    
    def FIFO(self):
        while(len(self.processos) > 0):
            for processo in self.processos:
                if (processo.getTempoChegada() <= self.time):
                    current = self.processos.popleft()
                    break

            while(not current.isEnded()):
                current.FIFO()
                for elem in self.processos:
                    if (elem.getTempoChegada() <= self.time):
                        elem.acumular()
                self.time +=1
            self.turnaround += current.getTempoTotal()
            self.ended.append(current)
        
        self.turnaround /= len(self.ended)
        print(self.turnaround)
        
        


simulador = Simulador()
simulador.criarProcesso(0, 4, 7, 2, 10)
simulador.criarProcesso(2, 2, 5, 2, 10)
simulador.criarProcesso(4, 1, 8, 2, 10)
simulador.criarProcesso(6, 3, 10, 2, 10)


simulador.FIFO()
