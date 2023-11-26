from Processo import Processo
from tkinter import *
from tkinter import ttk, font
from collections import deque
from Processador import Processador

class Entry_int(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit(): 
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.set(self.old_value)


class Simulador(Tk):

    def __init__(self, width, heigth):
        super().__init__()

        self.width = width
        self.heigth = heigth

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        x = ( self.screen_width/2) - (self.width/2)
        y = ( self.screen_height/2) - (self.heigth/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.heigth, x- self.screen_width/5, y- self.screen_height/5))
        self.title("Escalonador de processos")
        
        #widgets do tkinter
        self.widgets = {}
        self.buttons:dict[str, Button] = {}      #autoexplicativo

        #iniciar as variavels como None é como usar um NULLPOINTER, é interessante pra inicializar atributos de classes.
        self.quantum = None
        self.sobrecarga = None
        self.quantum_entry = None
        self.sobrecarga_entry = None

        #lista de labels que vai ser percorrida pra mostrar as informações na tela
        self.memoryLabels:list[Label] = []
        self.diskLabels:list[Label] = []

        self.cpu = Processador()   #como a cpu vai ser fixa podemos iniciar logo
        self.processos:deque[Processo] = deque()    #fila de processos que será capturada a partir da entrada do usuario

        self.selected = []    #aqui ficara o conjunto de processos selecionados pelo usuario (o unico uso é excluir o processo)
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
        self.widgets['TREEVIEW'] = ttk.Treeview(self, columns=("id","chegada", "exec", "prio", "deadline", "paginas"), show="headings", height=16)
        self.widgets['TREEVIEW'].bind("<<TreeviewSelect>>", self.on_select)
        self.widgets['TREEVIEW'].column("id", minwidth=0, width=30)
        self.widgets['TREEVIEW'].column("chegada", minwidth=0, width=120)
        self.widgets['TREEVIEW'].column("exec", minwidth=0, width=120)
        self.widgets['TREEVIEW'].column("prio", minwidth=0, width=100)
        self.widgets['TREEVIEW'].column("deadline", minwidth=0, width=100)
        self.widgets['TREEVIEW'].column("paginas", minwidth=0, width=100)
        self.widgets['TREEVIEW'].heading("id", text="ID")
        self.widgets['TREEVIEW'].heading("chegada", text="Tempo de Chegada")
        self.widgets['TREEVIEW'].heading("exec", text="Tempo de Execução")
        self.widgets['TREEVIEW'].heading("prio", text="Prioridade")
        self.widgets['TREEVIEW'].heading("deadline", text="Deadline")
        self.widgets['TREEVIEW'].heading("paginas", text="Nº Paginas")
        self.widgets['TREEVIEW'].grid(row=0, column=0, padx=10, pady=10)
        
    def createBoxWidgets(self):
        Label(self, text="Algoritmos", width=11).place(x=598,y=160)
        algoritmos_processos = ["FIFO", "RoundRobin", "SJF", "EDF"]
        self.widgets['BOX_ALGORITMOS'] = ttk.Combobox(self, values=algoritmos_processos)
        self.widgets['BOX_ALGORITMOS'].place(x=590,y=180, width=100)
        
        Label(self, text="Paginação", width=11).place(x=598,y=210)
        algoritmos_paginacao = ["FIFO", "LRU"]
        self.widgets['BOX_PAGINAS'] = ttk.Combobox(self, values=algoritmos_paginacao)
        self.widgets['BOX_PAGINAS'].place(x=590, y=230, width=100)        

    def createButtonsWidget(self):
        self.buttons['START'] = Button(self, text ="START", relief="raised",command=self.startAction)
        self.buttons['START'].place(x=590, y=330, width=100)
        self.buttons['CREATE_PROCESS'] = Button(self, text ="Criar Processo", relief="raised", command=self.criarProcesso)
        self.buttons['CREATE_PROCESS'].place(x=590, y=10, width=100)
        self.buttons['DELETE_PROCESS'] = Button(self, text ="Excluir Processo", relief="raised",command=self.delete_selected)
        self.buttons['DELETE_PROCESS'].place(x=590, y=45, width=100)

    def createTextBoxWidget(self):
        ttk.Label(self, text= "Quantum").place(x=610, y=78, width=100)
        self.quantum_entry = Entry_int(self, width=5)
        self.quantum_entry.place(x=590, y=95, width=100)

        ttk.Label(self, text= "Sobrecarga").place(x=605, y=118, width=100)
        self.sobrecarga_entry = Entry_int(self, width=5)
        self.sobrecarga_entry.place(x=590, y=135, width=100)
        
    def createSlider(self):
        self.widgets['SLIDER'] = Scale(self, from_=0.125, to=2,
                            orient=HORIZONTAL, resolution=0.125, digits=4)
        self.widgets['SLIDER'].set(0.700)
        self.widgets['SLIDER'].place(x=590, y=260, width=100)
        ttk.Label(self, text= "Segundos").place(x=612, y=300, width=95)
    
    def on_select(self, event):
        self.selected = event.widget.selection()
    
    def delete_selected(self):
        need_delection = []
        for idx in self.selected:
            need_delection.append(self.widgets['TREEVIEW'].item(idx)['values'][0])
        
        for element in need_delection:
            selected = None
            for process in self.processos:
                if (process.getId() == element):
                    selected = process
                    break
            if (selected is not None):
                self.processos.remove(selected)
                selectedVaribale = self.widgets['TREEVIEW'].selection()
                self.widgets['TREEVIEW'].delete(selectedVaribale)

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

        action = self.widgets['BOX_ALGORITMOS'].get()
        if(action == "FIFO"):
            max_time = self.FIFO()
        elif(action == "SJF"):
            max_time = self.SJF()
        elif(action == "RoundRobin"):
            max_time = self.RoundRobin()
        elif(action == "EDF"):
            max_time = self.EDF()
        
        processWindow = Toplevel(self)
        x = ( self.screen_width/2) - (self.width/2)
        y = ( self.screen_height/2) - (self.heigth/2)
        height = (len(self.processos) * 33) + 50
        processWindow.geometry('%dx%d+%d+%d' % (self.width, height, x- self.screen_width/5, y- self.screen_height/5 + 410))
        processWindow.title(" Visualização")

        def on_closing():
            self.buttons['START'].config(state=NORMAL)
            processWindow.destroy()

        processWindow.protocol("WM_DELETE_WINDOW", on_closing)

        hframe = ttk.Frame(processWindow)

        scrollbar = ttk.Scrollbar(processWindow, orient="horizontal")
        scrollbar.pack(fill=X, side=BOTTOM, expand=False)

        mycanvas = Canvas(hframe, highlightthickness=0, width=680, height=200, xscrollcommand=scrollbar.set)
        mycanvas.pack(side=TOP, fill=BOTH, expand=True)

        scrollbar.config(command=mycanvas.xview)

    
        processWindowFrame = ttk.Frame(mycanvas, borderwidth=1, relief="solid")
        def configure_interior(event):
            size = (processWindowFrame.winfo_reqwidth(), processWindowFrame.winfo_reqheight())
            mycanvas.config(scrollregion=(0,0,size[0],size[1]))
            if(processWindowFrame.winfo_reqheight() != mycanvas.winfo_reqheight()):
                mycanvas.config(height=processWindowFrame.winfo_reqheight())

        def configure_canvas(event):
            if (processWindowFrame.winfo_reqheight() != mycanvas.winfo_reqheight()):
                mycanvas.itemconfigure(idFrame, height=mycanvas.winfo_reqheight())
        processWindowFrame.bind('<Configure>', configure_interior)
        mycanvas.bind('<Configure>', configure_canvas)
        idFrame = mycanvas.create_window(0,0,window = processWindowFrame, anchor=NW)

        hframe.pack()
        
        for i in range (max_time):
            Label(processWindowFrame,text=str(i), relief="groove", width=3).grid(row=0, column=i+1,ipady=5, pady=2)

        target:deque[Processo] = sorted(self.cpu.getEnded(), key=lambda x: x.id)
        for i in range(1, len(target)+1):
            Label(processWindowFrame, text="Processo "+ str(target[i-1].getId()), relief="groove").grid(row=i, column=0, ipady=5, ipadx=10, pady=1, padx= 2)

        memoryWindow = Toplevel(processWindow)
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

        def turnaround():
            def close_window():
                turnaround_screen.destroy()

            x = ( self.screen_width/2) - (40/2)
            y = ( self.screen_height/2) - (40/2)
            turnaround_screen = Toplevel(processWindow)
            turnaround_screen.geometry('%dx%d+%d+%d' % (40, 40, x, y))
            ttk.Label(turnaround_screen, text='Turnaround:'+ str(round(self.cpu.getTurnaround()/len(self.processos), 2))).pack()
            ttk.Button(turnaround_screen, text="OK", command=close_window).pack(expand=True)
        
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
                        Label(processWindowFrame, background=element[0], relief="ridge", width=3).grid(row=i, column=currentTime+1, ipady=5, sticky=EW)
                        ver = False
                        break
                if(ver and currentTime < max_time):
                    Label(processWindowFrame, background="gray", relief="ridge", width=3).grid(row=i, column=currentTime+1, ipady=5, sticky=EW)
                i +=1
            if (currentTime < max_time):
                processWindowFrame.after(int(1000* self.widgets['SLIDER'].get()), clock, currentTime+1, processList, memoryList, diskList)   #o delay ocorre aqui
            else:
                k=0
                for i in range(5):
                    for j in range(10):
                        self.memoryLabels[k].config(text="-", bg="white")
                        k+=1
                turnaround()
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
        #captura informações da criação do processo digitada pelo usuario
        def submit():
            tempoExec = int(exec_entry.get())
            tempoCheg = int(chegada_entry.get())
            prio = int(deadline_entry.get())
            dead = int(prioridade_entry.get())
            pag = int(pagina_entry.get())

            processo = Processo(self.id, tempoCheg, tempoExec, prio, dead, pag)
            self.id +=1
            processo.createLabel(self.widgets['TREEVIEW'])
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

        ttk.Label(newWindow, text= "Tempo de Execução: ").place(x=10,y=10, width=120)
        exec_entry = Entry_int(newWindow, width=5)
        exec_entry.place(x=130,y=10)

        ttk.Label(newWindow, text= "Tempo de Chegada: ").place(x=13,y=35, width=120)
        chegada_entry = Entry_int(newWindow, width=5)
        chegada_entry.place(x=130,y=35)

        ttk.Label(newWindow, text= "Deadline: ").place(x=40,y=60, width=100)
        deadline_entry = Entry_int(newWindow, width=5)
        deadline_entry.place(x=130,y=60)

        ttk.Label(newWindow, text= "Prioridade: ").place(x=35,y=85, width=100)
        prioridade_entry = Entry_int(newWindow, width=5)
        prioridade_entry.place(x=130,y=85)

        ttk.Label(newWindow, text= "Nº de Páginas: ").place(x=25,y=110, width=100)
        pagina_entry = Entry_int(newWindow, width=5)
        pagina_entry.place(x=130,y=110)

        ttk.Button(newWindow, text="Criar", command=submit).place(x=100,y=140, width=70)
        ttk.Button(newWindow, text="Cancelar", command=cancel).place(x=10,y=140, width=70)

    def FIFO(self):
        self.cpu.start(self.processos, self.widgets['BOX_PAGINAS'].get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess()
                self.cpu.calculateProcessTime(mode= "FIFO",)
        return self.cpu.getTime()
        
    def RoundRobin(self):
        self.cpu.start(self.processos, self.widgets['BOX_PAGINAS'].get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess()
                self.cpu.calculateProcessTime(mode= "RR", quantum=self.quantum, sobrecarga=self.sobrecarga)
        return self.cpu.getTime()
            
    def SJF(self):
        self.cpu.start(self.processos, self.widgets['BOX_PAGINAS'].get())
        while(not self.cpu.isEnded()):
            if(self.cpu.isQueueEmpty()):
                self.cpu.setTime(self.cpu.getTime() + 1)
                self.cpu.checkProcessQueue()
            else:
                self.cpu.chooseProcess(lower=True)
                self.cpu.calculateProcessTime(mode= "SJF", quantum=self.quantum, sobrecarga=self.sobrecarga)
        return self.cpu.getTime()

    def EDF(self):
        self.cpu.start(self.processos, self.widgets['BOX_PAGINAS'].get())
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

        



