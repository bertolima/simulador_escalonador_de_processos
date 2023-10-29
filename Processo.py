from tkinter import *
from tkinter import ttk

class Processo:
    def __init__(self, identifier, tempoChegada:int, tempoExec:int, deadline:int, prioridade:int, paginas:int):
        self.tempoChegada = tempoChegada
        self.tempoExec = tempoExec
        self.deadline = deadline
        self.prioridade = prioridade
        self.paginas = paginas
        self.tempoTotal = 0
        self.tempoExecVar = tempoExec
        self.frame = None
        self.labels:list[ttk.Label] = []
        self.id = identifier
    
    def createLabel(self, target):
        target.insert("", "end", values=(self.id,self.tempoChegada, self.tempoExec, self.prioridade, self.deadline, self.paginas))
        
    
    def isEnded(self):
        if (self.tempoExecVar <= 0):
            return True
        return False
    
    def sobrecarga(self, window, time):
        self.tempoTotal +=1
        if(window):
            Label(window, background="red").grid(row=self.id+1, column=time+1, ipadx=11, ipady=5)

    
    def acumular(self, window=None, time=None):
        self.tempoTotal += 1
        if (window):
            Label(window, background="yellow").grid(row=self.id+1, column=time+1, ipadx=11, ipady=5)
            

    def executar(self, window=None, time=None):
        self.tempoExecVar -= 1
        self.tempoTotal += 1
        if(window):
            Label(window, background="green").grid(row=self.id+1, column=time+1, ipadx=11, ipady=5)
    
    def restart(self):
        self.tempoExecVar = self.tempoExec
        self.tempoTotal = 0
    
    def getTempoChegada(self):
        return self.tempoChegada
    def getTempoExec(self):
        return self.tempoExecVar
    def getDeadline(self):
        return self.deadline
    def getPrioridade(self):
        return self.prioridade
    def getTempoTotal(self):
        return self.tempoTotal
    
    def setTempoTotal(self, tempo):
        self.tempoTotal = tempo
    


