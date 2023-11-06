from collections import deque
from Processo import Processo
class Processador:
    def __init__(self):
        self.queue:deque[Processo] = None
        self.currentProcessQueue:deque[Processo] = deque()
        self.time = 0
        self.currentProcess:Processo = None
    
    def executar(processo:Processo, quantum):
        processo.executar()
    
    def start(self, process_queue:deque[Processo]):
        self.queue = deque(process_queue)
        self.time = 0

        self.checkProcessQueue()

    def checkProcessQueue(self):
        for process in self.queue:
            if(process.getTempoChegada() == self.time):
                self.currentProcessQueue.append(process)
        for process in self.currentProcessQueue:
            if(self.queue.count(process) > 0):
                self.queue.remove(process)
    
    def isQueueEmpty(self):
        if (self.currentProcessQueue):
            return False
        return True

    def isEnded(self):
        if (self.currentProcessQueue or self.queue):
            return False
        return True
    
    def chooseProcess(self, lower = False):
        if (self.currentProcess is None and self.currentProcessQueue):
            if (not lower):
                self.currentProcess = self.currentProcessQueue.popleft()
            else:
                maxValue = float('inf')
                for process in self.currentProcessQueue:
                    if (process.getTempoExec() < maxValue):
                        maxValue = process.getTempoExec()
                for process in self.currentProcessQueue:
                    if (process.getTempoExec() == maxValue):
                        self.currentProcess = process
                        break
                self.currentProcessQueue.remove(self.currentProcess)

    def startProcess(self, mode, target = None, quantum = None, sobrecarga = None):
            if (mode == "FIFO"):
                while (not self.currentProcess.isEnded()):
                    self.currentProcess.executar(target, self.time)
                    [processo.acumular(target, self.time) for processo in self.currentProcessQueue]
                    target.update()
                    target.after(700)
                    self.time += 1
                    self.checkProcessQueue()
                self.currentProcess = None

            elif(mode == "RR"):
                i = sobrecarga
                j = quantum
                turnaround = 0
                while(j > 0):
                    j -= 1
                    self.currentProcess.executar(target, self.time)
                    [processo.acumular(target, self.time) for processo in self.currentProcessQueue]
                    target.update()
                    target.after(700)
                    self.time += 1
                    self.checkProcessQueue()
                    if(self.currentProcess.isEnded()):
                        break
                if(not self.currentProcess.isEnded()):
                    self.currentProcess.sobrecarga(target, self.time)
                    [processo.acumular(target, self.time) for processo in self.currentProcessQueue]
                    target.update()
                    target.after(700)
                    self.time +=1
                    self.currentProcessQueue.append(self.currentProcess)
                else:
                    ret = self.currentProcess.getTempoTotal()
                    self.currentProcess = None
                    return ret
                    
                
                self.currentProcess = None

            elif(mode == "SJF"):
                while(not self.currentProcess.isEnded()):
                    self.currentProcess.executar(target, self.time)
                    [processo.acumular(target, self.time) for processo in self.currentProcessQueue]
                    target.update()
                    target.after(700)
                    self.time += 1
                    self.checkProcessQueue()
                self.currentProcess = None
        

    def calculateProcess(self, mode, quantum = None, sobrecarga = None):
        if (mode == "FIFO"):
                while (not self.currentProcess.isEnded()):
                    self.currentProcess.executar(time=self.time)
                    [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                    self.time += 1
                    self.checkProcessQueue()
                self.currentProcess = None
        elif (mode == "RR"):
            i = sobrecarga
            j = quantum
            while(j > 0):
                j -= 1
                self.currentProcess.executar(time=self.time)
                [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                self.time += 1
                self.checkProcessQueue()
                [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                if(self.currentProcess.isEnded()):
                    break
            if(not self.currentProcess.isEnded()):
                self.currentProcess.sobrecarga(time=self.time)
                self.time +=1
                self.currentProcessQueue.append(self.currentProcess)
            self.currentProcess = None
        elif (mode == "SJF"):
            while (not self.currentProcess.isEnded()):
                self.currentProcess.executar(time=self.time)
                [processo.acumular(time=self.time) for processo in self.currentProcessQueue]
                self.time += 1
                self.checkProcessQueue()
            self.currentProcess = None




    def getTime(self):
        return self.time
    
    def setTime(self,time):
        self.time = time



