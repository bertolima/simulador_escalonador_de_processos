from Processo import Processo
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
from collections import deque
from Processador import Processador



class Simulador(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x250")
        self.title("Escalonador de processos")

        self.quantum = None
        self.sobrecarga = None
        self.quantum_entry = None
        self.sobrecarga_entry = None
        self.cpu = Processador()

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

        for processo in self.processos:
            processo.restart()
        def getEntry():
            self.quantum = int(self.quantum_entry.get())
            self.sobrecarga = int(self.sobrecarga_entry.get())
        
        def createNewWindow(size):
            self.processWindow = Toplevel(self)
            self.processWindow.title(" Visualização")
            
            for i in range (max_time):
                Label(self.processWindow,text=str(i), relief="groove", width=3).grid(row=0, column=i+1,ipady=5)

            self.restart()

            for i in range(len(self.processos)):
                Label(self.processWindow, text="Processo "+ str(i), relief="groove").grid(row=i+1, column=0, ipady=5, ipadx=10, pady=1)

            
        
        getEntry()


        action = self.box.get()
        if(action == "FIFO"):
            max_time = self.FIFO(True)
            self.canRun = True
            createNewWindow(max_time)
            self.FIFO()
        elif(action == "SJF"):
            max_time = self.SJF(True)
            self.canRun = True
            createNewWindow(max_time)
            self.SJF()
        elif(action == "RoundRobin"):
            max_time = self.RoundRobin(True)
            self.canRun = True
            createNewWindow(max_time)
            self.RoundRobin()
        elif(action == "EDF"):
            max_time = self.EDF(True)
            self.canRun = True
            createNewWindow(max_time)
            self.EDF()


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
            

    def FIFO(self, calculo = False):
        if (not calculo):
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess()
                    self.cpu.startProcess(mode= "FIFO", target = self.processWindow)
        else:
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess()
                    self.cpu.calculateProcess(mode= "FIFO",)
            return self.cpu.getTime()
        

    def RoundRobin(self, calculo = False):
        if (not calculo):
            turnaround = 0
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess()
                    a = self.cpu.startProcess(mode= "RR", target=self.processWindow, quantum=self.quantum, sobrecarga=self.sobrecarga)
                    if (a is not None):
                        turnaround += a
            print(turnaround/len(self.processos))
        else:
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess()
                    self.cpu.calculateProcess(mode= "RR", quantum=self.quantum, sobrecarga=self.sobrecarga)
            return self.cpu.getTime()
            
        
        

    def SJF(self, calculo = False):
        if (not calculo):
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess(lower=True)
                    self.cpu.startProcess(mode= "SJF", target=self.processWindow, quantum=self.quantum, sobrecarga=self.sobrecarga)
        else:
            self.cpu.start(self.processos)
            while(not self.cpu.isEnded()):
                if(self.cpu.isQueueEmpty()):
                    self.cpu.setTime(self.cpu.getTime() + 1)
                else:
                    self.cpu.chooseProcess(lower=True)
                    self.cpu.calculateProcess(mode= "SJF", quantum=self.quantum, sobrecarga=self.sobrecarga)
            return self.cpu.getTime()
        

    def EDF(self, calculo = False):
        pass

        



