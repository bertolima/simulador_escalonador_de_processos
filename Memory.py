from collections import deque
from Processo import *
class Memory:
    
    def __init__(self, algorithm, all_processes:dict): # dicionário {Processo: Nº Páginas}
        
        self.diskSize = 200 # tamanho inicial do Disco
        self.disk = ["-"]*200 # criando array "vazio" ("-" vai representar o vazio)
        
        self.pages = self.allocateAllPages(all_processes) # aloco todos os processos no disco
        
        self.memorySize = 50
        self.memory = ["-"]*50
        
        self.algorithm = algorithm # FIFO ou LRU
        self.freeSpace = self.memorySize # monitoramento do espaço livre na memória
        self.queue = deque() # fila para gerenciar quando houver page fault
        self.mode = None
        self.count = 0
        
    def allocateAllPages(self, all_processes:dict): # dicionário {Processo: Nº Páginas}
        pages = 0
        
        # aloco os processos na ordem da lista 
        for process in all_processes:
            process_pages = all_processes[process]
            for i in range(process_pages):
                self.disk[i + pages] = process.getId()
            
            pages += process_pages 
        
        return pages
    
    
    def hasContinuosSpace(self, process:Processo): # calcula se tem espaço contínuo (não fragmentado) na memória 
        start = 0
        end = 0
        out = False
        for i in range(self.memorySize):
            if (end - start) == process.getPaginas(): # quando achar um espaço, sai do loop
                out = True
                break
            
            if self.memory[i] == "-": # vai aumentando a referência de fim conforme acha espaços vazios
                end += 1
            else: # se encontrar algo que não seja vazio, reinicia
                start = i
                end = i
        
        return out
        
            
    def reallocateInDisk(self, process:Processo): # método para tirar processo da memória e por no disco
        print("\n --------- Realocando processo", process.getId(), "no disco ---------- \n")
        i = self.memory.index(process.getId())
        last_page = i + process.getPaginas()
        
        while (i < last_page): # percorre todas as páginas do processo e coloca "-" 
            self.memory[i] = "-"
            i+=1
        print("Memória alterada para:")
        print(self.memory) 
        # usei esse mecanismo de start e end para encontrar o primeiro espaço livre do disco que caiba o processo inteiro, sem fragmentação 
        
        start = 0
        end = 0
        for i in range(self.diskSize):
            if (end - start) == process.getPaginas(): # quando achar um espaço, sai do loop
                break
            
            if self.disk[i] == "-": # vai aumentando a referência de fim conforme acha espaços vazios
                end += 1
            else: # se encontrar algo que não seja vazio, reinicia
                start = i+1
                end = i+1
        
        while (start < end): # itera sobre esse espaço colocando as páginas no disco
            self.disk[start] = process.getId()
            start += 1
            
        print("Disco alterado para:")
        print(self.disk)
        
    def removeFromDisk(self, process:Processo): # remove processo do disco para levar à memória
        i = self.disk.index(process.getId())
        last_page = i + process.getPaginas()
        
        while (i < last_page):
            self.disk[i] = "-"
            i+=1
    
    
    def allocateInMemory(self, process:Processo): # aloca o processo na memória
        if process.getId() in self.memory: # se o processo já tiver na memória, não faz nada
            return
              
        # -- NÃO ESTÁ NA MEMÓRIA --
        
        
        print('Disco')
        print(self.disk)
        print('Memória')
        print(self.memory)
        
        print('Fila no momento:', self.count)
        for i in self.queue:
            print(i.getId(), end=" ")
        print()
        self.count += 1
        
        self.removeFromDisk(process=process) # tiro o processo do disco para transferir à memória
        
        if self.hasContinuosSpace(process=process): # se tiver espaço contínuo (não fragmentado) suficiente, coloco direto, sem precisar do algoritmo
            print('Tem espaço contínuo')
            # procura pelo espaço inicial e final da memória, onde o processo será alocado
            start = 0
            end = 0
            for i in range(self.memorySize):
                if (end - start) == process.getPaginas(): # quando achar um espaço, sai do loop
                    break
                
                if self.memory[i] == "-": # vai aumentando a referência de fim conforme acha espaços vazios
                    end += 1
                else: # se encontrar algo que não seja vazio, reinicia
                    start = i+1
                    end = i+1
            
            while (start < end): # itera sobre esse espaço colocando as páginas no disco
                self.memory[start] = process.getId()
                start += 1
            
            self.freeSpace -= process.getPaginas() # diminuo o contador de espaço livre na memória
            self.queue.append(process) # adiciono na fila de processos para o FIFO

        else:
            print('Não tem espaço contínuo')
            if self.algorithm == "FIFO":
                print("\nENTROU NO FIFO\n")
                space_to_be_realocated = self.queue[0].getPaginas() # espaço que vou calcular se é suficiente para por o novo processo no lugar
                                
                while(space_to_be_realocated < process.getPaginas()): # se não for suficiente, vou dropar quantos processos forem necessários para caber o novo processo
                    self.reallocateInDisk(process=self.queue[0]) # realoco no disco o primeiro processo da fila
                    self.queue.popleft() # pop
                    space_to_be_realocated += self.queue[0].getPaginas() # novo espaço para realocação
                    
                self.freeSpace += space_to_be_realocated # aumento o espaço o livre
                self.reallocateInDisk(process=self.queue[0]) # realoco o último processo necessário no disco
                self.queue.popleft() # pop    
                
                # acho o primeiro espaço livre após as remoções da memória
                i = self.memory.index("-")
                last_page = i + process.getPaginas()
                
                while(i<last_page): # aloco todas as páginas do processo na memória
                    self.memory[i] = process.getId()
                    i+=1
                
                
                self.freeSpace -= process.getPaginas() # diminuo o espaço livre
                self.queue.append(process) # adiciono na fila de processos para o FIFO
        
            
    def getMemory(self):
        return self.memory
    
    
    def getDisk(self):
        return self.disk
    
    def desallocateProcess(self, process:Processo):
        self.queue.remove(process)
        for i in range(len(self.memory)):
            if(self.memory[i] == process.getId()):
                self.memory[i] = "-"

        for elem in self.disk:
            if elem == process.getId():
                elem = "-"
