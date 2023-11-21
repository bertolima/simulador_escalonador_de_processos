from collections import deque
from Processo import Processo
from Memory import Memory
import threading

class Processador:
    
    def __init__(self):
        
        self.queue:deque[Processo] = None   #representa a fila de todos os processs a serem executados
        self.currentProcessQueue:deque[Processo] = deque()  #simula a fila real de processos que chegam e devem ser executados na cpu
        self.time = 0   #clock do sistema
        self.currentProcess:Processo = None #Simula o processo que esta sendo executado no momento
        self.endedProcess = []  #processos ja finalizados entram aqui
        self.memory = None
        self.memoryLabels = deque()
        self.diskLabels = deque()
        
        

    #Note que todos esses mini-métodos se referem a apenas UM CLOCK, sendo a unidade clock igual a 1 segundo
    #Inicia a execução do processador com clock = 0 e a fila de processos zerada    
    def start(self, process_queue:deque[Processo], mode):
        self.queue = deque(process_queue)
        self.mode = mode
        process_dic = {}
        for process in self.queue:
            process_dic[process] = process.getPaginas()
        self.memory = Memory(mode, process_dic)
        self.time = 0
        self.endedProcess.clear()
        self.checkProcessQueue()

    #checa se naquele clock algum processo chegou a fila real
    def checkProcessQueue(self):
        for process in self.queue:
            if(process.getTempoChegada() == self.time):
                self.currentProcessQueue.append(process)
                self.memory.allocateInDisk(process)
        for process in self.currentProcessQueue:
            if(self.queue.count(process) > 0):
                self.queue.remove(process)

    #executa com 1 clock o processo atual
    def executar(processo:Processo, quantum):
        processo.executar()
    
    #escolhe o processo que vai ser executado pela CPU
    #A escolha do processo depende do algoritmo usado
    def chooseProcess(self, lower = False, prio = False):
        if (self.currentProcess is None and self.currentProcessQueue):
            if (not lower and not prio):
                self.currentProcess = self.currentProcessQueue.popleft() 

            elif(lower and not prio):
                maxValue = float('inf')
                for process in self.currentProcessQueue:
                    if (process.getTempoExec() < maxValue):
                        maxValue = process.getTempoExec()
                for process in self.currentProcessQueue:
                    if (process.getTempoExec() == maxValue):
                        self.currentProcess = process
                        break
                self.currentProcessQueue.remove(self.currentProcess)

            elif(not lower and prio):
                minValue = float('inf')
                for process in self.currentProcessQueue:
                    new_deadline = process.getDeadline() - process.getTempoTotal()
                    if(new_deadline < minValue):
                        minValue = new_deadline
                for process in self.currentProcessQueue:
                    if (process.getDeadline() - process.getTempoTotal() == minValue):
                        self.currentProcess = process
                        break
                self.currentProcessQueue.remove(self.currentProcess)
            memoryCurrentState = self.memory.getMemory()
            diskCurrentState = self.memory.getDisk()

            
            self.memory.allocateInMemory(self.currentProcess)
            for i in range(len(memoryCurrentState)):
                if memoryCurrentState[i] == "-":
                    self.memoryLabels.append((i, "white", self.time, "-"))
                elif (memoryCurrentState[i] == self.currentProcess.getId()):                
                    self.memoryLabels.append((i, self.currentProcess.getColor(), self.time, self.currentProcess.getId()))
            for i in range(len(diskCurrentState)):
                if diskCurrentState[i] == "-":
                    self.diskLabels.append((i, "white", self.time, "-"))
                else: 
                    self.diskLabels.append((i, self.currentProcess.getColor(), self.time, diskCurrentState[i]))
            
            
            

            

    #aqui todo funcionamento do sistema é feito "por debaixo dos panos" e as informações de como deverá ser renderizado
    #ficam dentro das instancias de cada um do processo guardados na fila "LabelList", a partir dessa fila é feita a
    #atualização e renderização na tela. E claro, depende do algoritmo escolhido.
    def calculateProcessTime(self, mode, quantum = None, sobrecarga = None):
        if (mode == "FIFO"):
                while (not self.currentProcess.isEnded()):
                    self.currentProcess.executar(time=self.time)
                    [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                    self.time += 1
                    self.checkProcessQueue()
                self.endedProcess.append(self.currentProcess)
                self.memory.desallocateProcess(self.currentProcess)
                self.currentProcess = None

        elif (mode == "RR"):
            i = sobrecarga
            j = quantum
            turnaround = 0
            while(j > 0):
                j -= 1
                self.currentProcess.executar(self.time)
                [processo.acumular(self.time) for processo in self.currentProcessQueue]
                self.time += 1
                self.checkProcessQueue()
                if(self.currentProcess.isEnded()):
                    self.endedProcess.append(self.currentProcess)
                    self.memory.desallocateProcess(self.currentProcess)
                    break
            if(not self.currentProcess.isEnded()):
                self.currentProcess.sobrecarga(self.time)
                [processo.acumular(self.time) for processo in self.currentProcessQueue]
                self.time +=1
                self.checkProcessQueue()
                self.currentProcessQueue.append(self.currentProcess)
                
            else:
                ret = self.currentProcess.getTempoTotal()
                self.currentProcess = None
                return ret
            self.currentProcess = None


        elif (mode == "SJF"):
            while (not self.currentProcess.isEnded()):
                self.currentProcess.executar(time=self.time)
                [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                self.time += 1
                self.checkProcessQueue()
            self.endedProcess.append(self.currentProcess)
            self.memory.desallocateProcess(self.currentProcess)
            self.currentProcess = None

        elif (mode == "EDF"):
            i = sobrecarga
            j = quantum
            turnaround = 0
            while(j > 0):
                j -= 1
                self.currentProcess.executar(self.time)
                [processo.acumular(self.time) for processo in self.currentProcessQueue]
                self.time += 1
                self.checkProcessQueue()
                if(self.currentProcess.isEnded()):
                    self.memory.desallocateProcess(self.currentProcess)
                    break
            if(not self.currentProcess.isEnded()):
                self.currentProcess.sobrecarga(self.time)
                [processo.acumular(self.time) for processo in self.currentProcessQueue]
                self.time +=1
                self.checkProcessQueue()
                self.currentProcessQueue.append(self.currentProcess)
            else:
                self.endedProcess.append(self.currentProcess)
                ret = self.currentProcess.getTempoTotal()
                self.currentProcess = None
                return ret
            self.currentProcess = None

    #accesors and modifiers
    def getEnded(self):
        return self.endedProcess

    def isQueueEmpty(self):
        if (self.currentProcessQueue):
            return False
        return True

    def isEnded(self):
        if (self.currentProcessQueue or self.queue):
            return False
        return True

    def getTime(self):
        return self.time
    
    def setTime(self,time):
        self.time = time
    
    def getMemoryLabels(self):
        return self.memoryLabels
    
    def resetMemoryLabels(self):
        self.memoryLabels.clear()
        self.diskLabels.clear()

    def getDiskLabels(self):
        return self.diskLabels



