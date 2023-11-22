from tkinter import *

class Processo:

    def __init__(self, identifier, tempoChegada:int, tempoExec:int, deadline:int, prioridade:int, paginas:int):
        #variaveis autoexplicativas
        self.id = identifier
        self.tempoChegada = tempoChegada
        self.tempoExec = tempoExec
        self.deadline = deadline
        self.prioridade = prioridade
        self.paginas = paginas
        self.tempoTotal = 0

        #aqui é o calculado o tempo restante que o processo tem a ser executado
        self.tempoExecVar = tempoExec

        #lista de labeis para renderizar a execução do processo na tela.
        self.labelList = []

    #Label criado para amostragem do processo na tela.
    def createLabel(self, target):
        target.insert("", "end", values=(self.id,self.tempoChegada, self.tempoExec, self.prioridade, self.deadline, self.paginas))

    #simula sobrecarga do processo em UM CLOCK
    def sobrecarga(self,time=None):
        self.tempoTotal +=1
        self.labelList.append(("red", time, self.id))

    #simula UM CLOCK de tempo de espera do processo
    def acumular(self, time=None):
        self.tempoTotal += 1
        self.labelList.append(("yellow", time, self.id))
            
    #executa o processo em UM CLOCK
    def executar(self, time=None):
        self.tempoExecVar -= 1
        self.tempoTotal += 1
        self.labelList.append(("green", time, self.id))
    
    #checa se aquele processo já acabou
    def isEnded(self):
        if (self.tempoExecVar <= 0):
            return True
        return False
    
    #reinicia os status do processo
    def restart(self):
        self.tempoExecVar = self.tempoExec
        self.tempoTotal = 0
        self.labelList.clear()

    #acessors and modifiers
    def getId(self):
        return self.id
    
    def getLabelList(self):
        return self.labelList

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
    
    def getPaginas(self):
        return self.paginas

