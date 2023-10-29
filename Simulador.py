from Processo import Processo
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from collections import deque



class Simulador(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x250")
        self.title("Escalonador de processos")

        self.quantum = None
        self.sobrecarga = None
        self.quantum_entry = None
        self.sobrecarga_entry = None

        self.processos:deque[Processo] = deque()
        self.processos.append(Processo(0, 0, 4, 1, 1, 1))
        self.processos.append(Processo(1, 2, 2, 1, 1, 1))
        self.processos.append(Processo(2, 4,1, 1, 1,1))
        self.processos.append(Processo(3, 6, 3, 1, 1, 1))
        
        self.processWindow = None
        self.ended = []
        self.turnaround = 0
        self.time = 0
        self.processTree = None
        self.box = None
        self.butttons = []
        self.id = 0
        self.canRun = False
        self.initWidgets()

      
    def initWidgets(self):
        self.createTreeWidget()
        self.createBoxWidget()
        self.createButtonsWidget()
        self.createTextBoxWidget()

    def createTreeWidget(self):
        self.processTree = ttk.Treeview(self, columns=("id","chegada", "exec", "prio", "deadline", "paginas"), show="headings")
        self.processTree.column("id", minwidth=0, width=30)
        self.processTree.column("chegada", minwidth=0, width=120)
        self.processTree.column("exec", minwidth=0, width=120)
        self.processTree.column("prio", minwidth=0, width=100)
        self.processTree.column("deadline", minwidth=0, width=100)
        self.processTree.column("paginas", minwidth=0, width=100)
        self.processTree.heading("id", text="ID")
        self.processTree.heading("chegada", text="Tempo de Chegada")
        self.processTree.heading("exec", text="Tempo de Execução")
        self.processTree.heading("prio", text="Prioridade")
        self.processTree.heading("deadline", text="Deadline")
        self.processTree.heading("paginas", text="Nº Paginas")
        self.processTree.place(x=10,y=10)

    def createBoxWidget(self):
        Label(self, text="Algoritmos").place(x=608,y=160)
        algoritmos = ["FIFO", "RoundRobin", "SJF", "EDF"]
        self.box = ttk.Combobox(self, values=algoritmos)
        self.box.place(x=595,y=180, width=95)

    def createButtonsWidget(self):
        Button(self, text ="START", relief="raised",command=self.startAction).place(x=595, y=210, width=95)
        Button(self, text ="Criar Processo", relief="raised", command=self.criarProcesso).place(x=595, y=10, width=95)
        Button(self, text ="Deletar Processo", relief="raised",command=self.deleteProcess).place(x=595, y=45, width=95)

    def createTextBoxWidget(self):
        chegada_label = ttk.Label(self, text= "Quantum").place(x=612, y=75, width=95)
        self.quantum_entry = ttk.Entry(self, width=5)
        self.quantum_entry.place(x=595, y=95, width=95)

        exec_label = Label(self, text= "Sobrecarga").place(x=593, y=115, width=95)
        self.sobrecarga_entry = Entry(self, width=5)
        self.sobrecarga_entry.place(x=595, y=135, width=95)

    def deleteProcess(self):
        selected = self.processTree.selection()
        print(selected)
        self.processTree.delete(selected)


    def startAction(self):
        def getEntry():
            self.quantum = int(self.quantum_entry.get())
            self.sobrecarga = int(self.sobrecarga_entry.get())
        
        def createNewWindow(size):
            self.processWindow = Toplevel(self)
            self.processWindow.title(" Visualização")
            
            for i in range (max_time):
                Label(self.processWindow,text=str(i), relief="groove").grid(row=0, column=i+1, ipadx=10, ipady=5)

            self.restart()

            for i in range(len(self.processos)):
                Label(self.processWindow, text="Processo "+ str(i), relief="groove").grid(row=i+1, column=0, ipady=5, ipadx=10, pady=1)

            self.FIFO()
    

        
        getEntry()

        max_time = self.calcularTempo()
        self.canRun = True

        createNewWindow(max_time)

            

        # action = self.box.get()
        # if(action == "FIFO"): self.FIFO(self.processWindow)
        # elif(action == "SJF"): self.SJF()
        # elif(action == "RoundRobin"): self.RoundRobin()
        # elif(action == "EDF"): self.EDF()





    def criarProcesso(self):
        
        newWindow = Toplevel(self)
        newWindow.title(" Janela de Criação de Processo")
        newWindow.geometry("180x175")

        def submit():
            tempoExec = int(exec_entry.get())
            tempoCheg = int(chegada_entry.get())
            prio = int(deadline_entry.get())
            dead = int(prioridade_entry.get())
            pag = int(pagina_entry.get())

            processo = Processo(self.id, tempoCheg, tempoExec, prio, dead, pag)
            self.id +=1
            processo.createLabel(self.processTree)
            self.processos.append(processo)
            newWindow.destroy()
        
        def cancel():
            newWindow.destroy()
        
    
        exec_label = Label(newWindow, text= "Tempo de Execução: ").place(x=10,y=10, width=120)
        exec_entry = Entry(newWindow, width=5)
        exec_entry.place(x=130,y=10)

        chegada_label = ttk.Label(newWindow, text= "Tempo de Chegada: ").place(x=13,y=35, width=120)
        chegada_entry = ttk.Entry(newWindow, width=5)
        chegada_entry.place(x=130,y=35)

        deadline_label = ttk.Label(newWindow, text= "Deadline: ").place(x=40,y=60, width=100)
        deadline_entry = ttk.Entry(newWindow, width=5)
        deadline_entry.place(x=130,y=60)

        prioridade_label = ttk.Label(newWindow, text= "Prioridade: ").place(x=35,y=85, width=100)
        prioridade_entry = ttk.Entry(newWindow, width=5)
        prioridade_entry.place(x=130,y=85)

        pagina_label = ttk.Label(newWindow, text= "Nº de Páginas: ").place(x=25,y=110, width=100)
        pagina_entry = ttk.Entry(newWindow, width=5)
        pagina_entry.place(x=130,y=110)

    
        submit_button = ttk.Button(newWindow, text="Criar", command=submit).place(x=100,y=140, width=70)
        submit_button = ttk.Button(newWindow, text="Cancelar", command=cancel).place(x=10,y=140, width=70)











































    def restart(self):
        for elem in self.processos:
            elem.restart()
            

    def verificarProcesso(self, processList:list[Processo], time):
        aux = deque()
        for process in processList:
            if(process.getTempoChegada() == time):
                aux.appendleft(process)
        for process in aux:
            if(processList.count(process) > 0):
                processList.remove(process)
        
        return aux

    def calcularTempo(self):
        process_queue = deque(self.processos)
        time = 0

        while (process_queue):
            current = None
            for process in process_queue:
                if (process.getTempoChegada()<= time):
                    current = process
                    break
            if (current):
                process_queue.remove(current)
                while(not current.isEnded()):
                    current.executar()
                    [process.acumular() for process in process_queue if process.getTempoChegada() <= time]
                    time +=1
            else:
                time += 1
        return time


    def FIFO(self):
        process_queue = deque(self.processos)
        time = 0

        while (process_queue):
            current = None
            for process in process_queue:
                if (process.getTempoChegada()<= time):
                    current = process
                    break
            if (current):
                process_queue.remove(current)
                while(not current.isEnded()):
                    current.executar(self.processWindow, time)
                    [process.acumular(self.processWindow, time) for process in process_queue if process.getTempoChegada() <= time]
                    time +=1
            else:
                time += 1
        return time

        
    
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

        



