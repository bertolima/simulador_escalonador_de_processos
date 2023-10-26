from Processo import Processo
from tkinter import *
from tkinter import ttk
import time
from collections import deque



class Simulador(Tk):
    def __init__(self, quantum = None, sobrecarga = None):
        super().__init__()
        super().geometry("800x800")
        super().title("Escalonador de processos")
        self.quantum = quantum
        self.sobrecarga = sobrecarga
        self.processos:deque[Processo] = deque()
        self.ended = []
        self.turnaround = 0
        self.time = 0
        self.test()

    def criarProcesso(self):
        
        newWindow = Toplevel(self)
        newWindow.title(" Janela de Criação de Processo")
        def submit():
            tempoExec = int(exec_entry.get())
            tempoCheg = int(chegada_entry.get())
            prio = int(deadline_entry.get())
            dead = int(prioridade_entry.get())
            pag = int(pagina_entry.get())

            self.processos.append(Processo(tempoCheg, tempoExec, prio, dead, pag))
            newWindow.destroy()
        
    
        exec_label = Label(newWindow, text= "Tempo de Execução: ").grid(row=1,column=1)
        exec_entry = Entry(newWindow, width=5)
        exec_entry.grid(row=1,column=2)

        chegada_label = ttk.Label(newWindow, text= "Tempo de Chegada: ").grid(row=2,column=1)
        chegada_entry = ttk.Entry(newWindow, width=5)
        chegada_entry.grid(row=2,column=2)

        deadline_label = ttk.Label(newWindow, text= "Deadline: ").grid(row=3,column=1)
        deadline_entry = ttk.Entry(newWindow, width=5)
        deadline_entry.grid(row=3,column=2)

        prioridade_label = ttk.Label(newWindow, text= "Prioridade: ").grid(row=4,column=1)
        prioridade_entry = ttk.Entry(newWindow, width=5)
        prioridade_entry.grid(row=4,column=2)

        pagina_label = ttk.Label(newWindow, text= "Número de Páginas: ").grid(row=5,column=1)
        pagina_entry = ttk.Entry(newWindow, width=5)
        pagina_entry.grid(row=5,column=2)

        

        submit_button = ttk.Button(newWindow, text="Criar Processo", command=submit).grid(row=6,column=2)

        
        
    

        
        
        
    


    def test(self):
    
        btn = Button(self, text ="Criar Processo", command = self.criarProcesso)
        btn.grid(row=1,column=1)

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

        



