from Processo import Processo
from tkinter import *
from tkinter import ttk, font
from collections import deque
from Processador import Processador


class Simulador(Tk):

    def __init__(self, width, heigth):
        super().__init__()
        self.width = width
        self.heigth = heigth
        self.running = False
        self.canCreateProcess = True

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x = ( self.screen_width/2) - (self.width/2)
        y = ( self.screen_height/2) - (self.heigth/2)
        self.colors = ['gray', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'pink', 'purple']
        self.colorCounter = 0
        self.geometry('%dx%d+%d+%d' % (self.width, self.heigth, x- self.screen_width/5, y- self.screen_height/5))


        self.geometry("700x370")
        self.title("Escalonador de processos")
        
        #iniciar as variavels como None é como usar um NULLPOINTER, é interessante pra inicializar atributos de classes.
        self.quantum = None
        self.sobrecarga = None
        self.quantum_entry = None
        self.sobrecarga_entry = None
        self.pageBox = None
        self.slider = None
        self.memoryLabels:list[Label] = []
        self.diskLabels:list[Label] = []

        self.cpu = Processador()   #como a cpu vai ser fixa podemos iniciar logo
        self.processos:deque[Processo] = deque()    #fila de processos que será capturada a partir da entrada do usuario
        self.processos.append(Processo(0, 0, 7, 1, 1, 11, self.colors[0]))
        self.processos.append(Processo(1, 2, 8, 1, 1, 8, self.colors[1]))
        self.processos.append(Processo(2, 4,9, 1, 1,5, self.colors[2]))
        self.processos.append(Processo(3, 6, 6, 1, 1, 10, self.colors[3]))
        self.processos.append(Processo(4, 8, 5, 1, 1, 10, self.colors[4]))
        self.processos.append(Processo(5, 10, 3, 1, 1, 10, self.colors[5]))
        
        self.processWindow = None   #janela onde a execução dos processos será mostrada
        self.processTree = None     #arvore de exibição dos processos na main window
        self.selected = []          #aqui ficara o conjunto de processos selecionados pelo usuario (o unico uso é excluir o processo)
        self.processWindowFrame:ttk.Frame = None    #frame para exibição dos processos
        self.box = None     #vai representar a box onde poderemos escolher o algoritmo
        self.buttons:dict[str, Button] = {}      #autoexplicativo
        self.id = 0     #o contador unico para o ID dos processos

        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family="Helvetica", 
                                   size=8, 
                                   weight=font.BOLD,
                                   slant='roman') 
        self.initWidgets()      #inicializa todos os widgets principais da aplicação
        

    def initWidgets(self):
        self.createTreeWidget()
        self.createBoxWidgets()
        self.createButtonsWidget()
        self.createTextBoxWidget()
        self.createSlider()

    def createTreeWidget(self):
        self.processTree = ttk.Treeview(self, columns=("id","chegada", "exec", "prio", "deadline", "paginas"), show="headings", height=16)
        self.processTree.bind("<<TreeviewSelect>>", self.on_select)
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
        self.processTree.grid(row=0, column=0, padx=10, pady=10)

    def createBoxWidgets(self):
        Label(self, text="Algoritmos", width=11).place(x=598,y=160)
        algoritmos_processos = ["FIFO", "RoundRobin", "SJF", "EDF"]
        self.box = ttk.Combobox(self, values=algoritmos_processos)
        self.box.place(x=590,y=180, width=100)
        
        Label(self, text="Paginação", width=11).place(x=598,y=210)
        algoritmos_paginacao = ["FIFO", "LRU"]
        self.pageBox = ttk.Combobox(self, values=algoritmos_paginacao)
        self.pageBox.place(x=590, y=230, width=100)        

    def createButtonsWidget(self):
        self.buttons['START'] = Button(self, text ="START", relief="raised",command=self.startAction)
        self.buttons['START'].place(x=590, y=330, width=100)
        self.buttons['CREATE_PROCESS'] = Button(self, text ="Criar Processo", relief="raised", command=self.criarProcesso)
        self.buttons['CREATE_PROCESS'].place(x=590, y=10, width=100)
        self.buttons['DELETE_PROCESS'] = Button(self, text ="Excluir Processo", relief="raised",command=self.print_selected)
        self.buttons['DELETE_PROCESS'].place(x=590, y=45, width=100)

    def createTextBoxWidget(self):
        chegada_label = ttk.Label(self, text= "Quantum").place(x=610, y=75, width=100)
        self.quantum_entry = ttk.Entry(self, width=5)
        self.quantum_entry.place(x=590, y=95, width=100)

        exec_label = Label(self, text= "Sobrecarga").place(x=590, y=115, width=100)
        self.sobrecarga_entry = Entry(self, width=5)
        self.sobrecarga_entry.place(x=590, y=135, width=100)
        
    def createSlider(self):
        self.slider = Scale(self, from_=0.125, to=2,
                            orient=HORIZONTAL, resolution=0.125, digits=4)
        self.slider.set(0.700)
        self.slider.place(x=590, y=260, width=100)
        segundos_label = ttk.Label(self, text= "Segundos").place(x=612, y=300, width=95)
    
    def on_select(self, event):
        self.selected = event.widget.selection()
    
    def print_selected(self):
        need_delection = []
        for idx in self.selected:
            need_delection.append(self.processTree.item(idx)['values'][0])
        
        for element in need_delection:
            selected = None
            for process in self.processos:
                if (process.getId() == element):
                    selected = process
                    break
            if (selected is not None):
                self.processos.remove(selected)
                selectedVaribale = self.processTree.selection()
                self.processTree.delete(selectedVaribale)

    #esse método é invocado quando apertamos o botao "START"
    def startAction(self):

        self.buttons['START'].config(state=DISABLED)
        #reinicia o estado dos processos
        self.restart()
        self.cpu.resetMemoryLabels()
        self.memoryLabels.clear()
        self.diskLabels.clear()

        #captura a entrada do usuario sobre o quantum e sobrecarga
        self.quantum = int(self.quantum_entry.get())
        self.sobrecarga = int(self.sobrecarga_entry.get())

        action = self.box.get()
        if(action == "FIFO"):
            max_time = self.FIFO()
        elif(action == "SJF"):
            max_time = self.SJF()
        elif(action == "RoundRobin"):
            max_time = self.RoundRobin()
        elif(action == "EDF"):
            max_time = self.EDF()
        
        self.processWindow = Toplevel(self)
        x = ( self.screen_width/2) - (self.width/2)
        y = ( self.screen_height/2) - (self.heigth/2)
        height = (len(self.processos) * 40) + 5
        self.processWindow.geometry('%dx%d+%d+%d' % (self.width, height, x- self.screen_width/5, y- self.screen_height/5 + 410))
        self.processWindow.title(" Visualização")

        def on_closing():
            self.buttons['START'].config(state=NORMAL)
            self.processWindow.destroy()

        self.processWindow.protocol("WM_DELETE_WINDOW", on_closing)

        hframe = ttk.Frame(self.processWindow)

        scrollbar = ttk.Scrollbar(self.processWindow, orient="horizontal")
        scrollbar.pack(fill=X, side=BOTTOM, expand=False)

        mycanvas = Canvas(hframe, highlightthickness=0, width=680, height=200, xscrollcommand=scrollbar.set)
        mycanvas.pack(side=TOP, fill=BOTH, expand=True)

        scrollbar.config(command=mycanvas.xview)

    
        self.processWindowFrame = ttk.Frame(mycanvas, borderwidth=1, relief="solid")
        def configure_interior(event):
            size = (self.processWindowFrame.winfo_reqwidth(), self.processWindowFrame.winfo_reqheight())
            mycanvas.config(scrollregion=(0,0,size[0],size[1]))
            if(self.processWindowFrame.winfo_reqheight() != mycanvas.winfo_reqheight()):
                mycanvas.config(height=self.processWindowFrame.winfo_reqheight())

        def configure_canvas(event):
            if (self.processWindowFrame.winfo_reqheight() != mycanvas.winfo_reqheight()):
                mycanvas.itemconfigure(idFrame, height=mycanvas.winfo_reqheight())
        self.processWindowFrame.bind('<Configure>', configure_interior)
        mycanvas.bind('<Configure>', configure_canvas)
        idFrame = mycanvas.create_window(0,0,window = self.processWindowFrame, anchor=NW)

        hframe.pack()
        
        for i in range (max_time):
            Label(self.processWindowFrame,text=str(i), relief="groove", width=3).grid(row=0, column=i+1,ipady=5, pady=2)

        target:deque[Processo] = sorted(self.cpu.getEnded(), key=lambda x: x.id)
        for i in range(1, len(target)+1):
            Label(self.processWindowFrame, text="Processo "+ str(target[i-1].getId()), relief="groove").grid(row=i, column=0, ipady=5, ipadx=10, pady=1, padx= 2)

        memoryWindow = Toplevel(self.processWindow)
        memoryWindow.geometry('+%d+%d'%(x- self.screen_width/5 + 710, y- self.screen_height/5))
        memoryWindow.title("RAM e Disco")
        memoryFrame = ttk.Frame(memoryWindow, borderwidth=1, relief="solid", )
        memoryFrame.pack(padx=3, pady=3)
        diskFrame = ttk.Frame(memoryWindow, borderwidth=1, relief="solid", )
        diskFrame.pack(padx=3, pady=3)

        k=0
        for i in range(5):
            for j in range(10):
                self.memoryLabels.append(Label(memoryFrame, relief="groove", text="-", bg="white", width=3, height=2))
                self.memoryLabels[k].grid(row=i, column=j)
                k+=1

        k=0
        for i in range(10):
            for j in range(20):
                self.diskLabels.append(Label(diskFrame, relief="groove", text="-", bg="white", width=3, height=2))
                self.diskLabels[k].grid(row=i, column=j)
                k+=1


        
        #essa função é um chama ela novamente com um delay de 700ms
        #ela so continua a se chamar ate o tempo atual chegar no tempo maximo de execução dos processos
        def clock(currentTime, processList:list[Processo], memoryList:list, diskList:list):
            i = 1
            for elem in memoryList:
                    if elem[2] == currentTime:
                        self.memoryLabels[elem[0]].config(text = str(elem[3]), bg = elem[1])
            
            for elem in diskList:
                    if elem[2] == currentTime:
                        self.diskLabels[elem[0]].config(text = str(elem[3]), bg = elem[1])

            for process in processList:
                labelList = process.getLabelList()
                ver = True
                for element in labelList:
                    if element[1] == currentTime:
                        Label(self.processWindowFrame, background=element[0], relief="ridge", width=3).grid(row=i, column=currentTime+1, ipady=5, sticky=EW)
                        ver = False
                        break
                if(ver and currentTime < max_time):
                    Label(self.processWindowFrame, background="gray", relief="ridge", width=3).grid(row=i, column=currentTime+1, ipady=5, sticky=EW)
                i +=1
            if (currentTime < max_time):
                self.processWindowFrame.after(int(1000* self.slider.get()), clock, currentTime+1, processList, memoryList, diskList)   #o delay ocorre aqui
            else:
                k=0
                for i in range(5):
                    for j in range(10):
                        self.memoryLabels[k].config(text="-", bg="white")
                        k+=1
                self.buttons['START'].config(state=NORMAL)



        #serve pra chamar a função que renderizar as informações dos processos na tela
        #precisamos ordenar a lista de processos pelo ID antes, para que seja mostrado corretamente na tela
        def runProcess():
            target = sorted(self.cpu.getEnded(), key=lambda x: x.id)
            targetMemory = sorted(self.cpu.getMemoryLabels(), key = lambda x: x[2])
            targetDisk = sorted(self.cpu.getDiskLabels(), key = lambda x: x[2])
        
            time = 0
            clock(time, target, targetMemory, targetDisk)

        runProcess()

        

    #método acionado ao clicar no botao "CRIAR PROCESSO"
    def criarProcesso(self):
        if (not self.running):
            if (self.canCreateProcess):
                self.canCreateProcess = False
                #captura informações da criação do processo digitada pelo usuario
                def submit():
                    tempoExec = int(exec_entry.get())
                    tempoCheg = int(chegada_entry.get())
                    prio = int(deadline_entry.get())
                    dead = int(prioridade_entry.get())
                    pag = int(pagina_entry.get())

                    if(self.colorCounter == len(self.colors)): self.colorCounter = 0
                    processo = Processo(self.id, tempoCheg, tempoExec, prio, dead, pag, self.colors[self.colorCounter])
                    self.colorCounter+=1
                    self.id +=1
                    processo.createLabel(self.processTree)
                    self.processos.append(processo)
                    newWindow.destroy()
                    
                
                #autoexplicativo
                def cancel():
                    newWindow.destroy()
                

                #informações da janela criada para adicionar novos processos.
                newWindow = Toplevel(self)
                x = ( self.screen_width/2) - (180/2)
                y = ( self.screen_height/2) - (175/2)
                newWindow.geometry('%dx%d+%d+%d' % (180, 175, x- self.screen_width/5, y))
                newWindow.title(" Janela de Criação de Processo")
                newWindow.geometry("180x175")

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
                self.canCreateProcess = True


    def FIFO(self):
        self.cpu.start(self.processos, self.pageBox.get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess()
                self.cpu.calculateProcessTime(mode= "FIFO",)
        return self.cpu.getTime()
        

    def RoundRobin(self):
        self.cpu.start(self.processos, self.pageBox.get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess()
                self.cpu.calculateProcessTime(mode= "RR", quantum=self.quantum, sobrecarga=self.sobrecarga)
        return self.cpu.getTime()
            
        

    def SJF(self):
        self.cpu.start(self.processos, self.pageBox.get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess(lower=True)
                self.cpu.calculateProcessTime(mode= "SJF", quantum=self.quantum, sobrecarga=self.sobrecarga)
        return self.cpu.getTime()
        

    def EDF(self):
        self.cpu.start(self.processos, self.pageBox.get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess(prio=True)
                self.cpu.calculateProcessTime(mode= "EDF", quantum=self.quantum, sobrecarga=self.sobrecarga)
        return self.cpu.getTime()
    
    def restart(self):
        for elem in self.processos:
            elem.restart()

        



