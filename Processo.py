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
        self.id = identifier
        self.labelList = []
    
    def createLabel(self, target):
        target.insert("", "end", values=(self.id,self.tempoChegada, self.tempoExec, self.prioridade, self.deadline, self.paginas))
    
    def getId(self):
        return self.id
        
    
    def isEnded(self):
        if (self.tempoExecVar <= 0):
            return True
        return False
    
    def sobrecarga(self, window=None, time=None):
        self.tempoTotal +=1
        if(window):
            Label(window, background="red", relief="ridge", width=3).grid(row=self.id+1, column=time+1, ipady=5, sticky=EW)

    
    def acumular(self, window=None, time=None):
        self.tempoTotal += 1
        if (window):
            Label(window, background="yellow", relief="ridge", width=3).grid(row=self.id+1, column=time+1, ipady=5, sticky=EW)
            

    def executar(self, window=None, time=None):
        self.tempoExecVar -= 1
        self.tempoTotal += 1
        if(window):
            Label(window, background="green", relief="ridge", width=3).grid(row=self.id+1, column=time+1, ipady=5, sticky=EW)
    
    def restart(self):
        self.tempoExecVar = self.tempoExec
        self.tempoTotal = 0
    
    def getTempoChegada(self):
        return self.tempoChegada
    
    def getTempoExec(self):
        return self.tempoExecVar
    
    def getDeadline(self):
        return self.deadline
    
    def setDeadLine(self, value):
        self.deadline = value

    def getPrioridade(self):
        return self.prioridade
    
    def getTempoTotal(self):
        return self.tempoTotal
    
    def setTempoTotal(self, tempo):
        self.tempoTotal = tempo
    


