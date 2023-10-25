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
                current.executar()
                for elem in self.processos:
                    if (elem.getTempoChegada() <= self.time):
                        elem.acumular()
                self.time +=1
            self.turnaround += current.getTempoTotal()
            self.ended.append(current)
        
        self.turnaround /= len(self.ended)
        print(self.turnaround)
    
    def RoundRobin(self):
        processQueue:deque[Processo] = deque()
        
        def acumular():
            for processo in processQueue:
                processo.acumular()

        def verificarProcessos():
            for i in range (len(self.processos)):
                if (self.processos[i].getTempoChegada() == self.time):
                    processQueue.append(self.processos[i])

            for processo in processQueue:
                if (self.processos.count(processo) > 0):
                    self.processos.remove(processo)

        while(len(self.processos) > 0 or len(processQueue)):
            verificarProcessos()
            if(len(processQueue) > 0):
                current = processQueue.popleft()
                currentTime = self.quantum

                while(currentTime > 0 and not current.isEnded()):
                    current.executar()
                    acumular()
                    self.time +=1
                    currentTime-=1
                    verificarProcessos()
                
                if (current.isEnded()):
                    self.turnaround += current.getTempoTotal()
                    self.ended.append(current)
                    print(current.getTempoTotal())
                else:
                    current.setTempoTotal(current.getTempoTotal() + self.sobrecarga)
                    acumular()
                    self.time +=1
                    processQueue.append(current)

            else:
                self.time+=1
        
        self.turnaround /= len(self.ended)
        print(self.turnaround)

    def SJF(self):
        processQueue:deque[Processo] = deque()
        
        def acumular():
            for processo in processQueue:
                processo.acumular()

        def verificarProcessos():
            for i in range (len(self.processos)):
                if (self.processos[i].getTempoChegada() == self.time):
                    processQueue.append(self.processos[i])

            for processo in processQueue:
                if (self.processos.count(processo) > 0):
                    self.processos.remove(processo)
        
        def chooseMin():
            current = None
            i = 1000000000000000
            for j in range(len(processQueue)):
                if(processQueue[j].getTempoExec() < i ):
                    i = processQueue[j].getTempoExec()
            
            current = processQueue[j]
            processQueue.remove(current)
            return current
            

        while(len(self.processos) > 0 or len(processQueue)):
            verificarProcessos()
            if(len(processQueue) > 0):
                current = chooseMin()

                while(not current.isEnded()):
                    current.executar()
                    acumular()
                    self.time +=1
                    verificarProcessos()
                
                self.turnaround += current.getTempoTotal()
                self.ended.append(current)
            else:
                self.time+=1

    def EDF(self):
        pass

        



        




        
        


simulador = Simulador(2,1)
simulador.criarProcesso(0, 4, 7, 2, 10)
simulador.criarProcesso(2, 2, 5, 2, 10)
simulador.criarProcesso(4, 1, 8, 2, 10)
simulador.criarProcesso(6, 3, 10, 2, 10)


simulador.SJF()
