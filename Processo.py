

class Processo:
    def __init__(self, tempoChegada:int, tempoExec:int, deadline:int, prioridade:int, paginas:int):
        self.tempoChegada = tempoChegada
        self.tempoExec = tempoExec
        self.deadline = deadline
        self.prioridade = prioridade
        self.paginas = paginas
        self.tempoTotal = 0

        self.tempoExecVar = tempoExec
        self.ended = False
    
    def isEnded(self):
        return self.ended
    
    def acumular(self):
        self.tempoTotal += 1

    def FIFO(self):
        if (self.tempoExecVar > 0):
            self.tempoExecVar -= 1
            self.tempoTotal += 1

            if(self.tempoExecVar == 0):
                self.ended = True
    
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
    


