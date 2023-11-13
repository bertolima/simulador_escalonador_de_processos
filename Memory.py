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
        
    def allocateAllPages(self, all_processes:dict): # dicionário {Processo: Nº Páginas}
        pages = 0
        
        # aloco os processos na ordem da lista 
        for process in all_processes:
            process_pages = all_processes[process]
            for i in range(process_pages):
                self.disk[i + pages] = process.getId()
            
            pages += process_pages 
        
        return pages
            
    def reallocateInDisk(self, process:Processo): # método para tirar processo da memória e por no disco
        i = self.memory.index(process.getId())
        last_page = i + process.getPaginas()
        
        while (i < last_page): # percorre todas as páginas do processo e coloca "-" 
            self.memory[i] = "-"
            i+=1
        
        # usei esse mecanismo de start e end para encontrar o primeiro espaço livre do disco que caiba o processo inteiro, sem fragmentação 
        
        #TODO: transformar esse bloco inteiro num método, para usar na RAM também
        start = 0
        end = 0
        for i in range(self.diskSize):
            if (end - start) == process.getPaginas(): # quando achar um espaço, sai do loop
                break
            
            if self.disk[i] == "-": # vai aumentando a referência de fim conforme acha espaços vazios
                end += 1
            else: # se encontrar algo que não seja vazio, reinicia
                start = i
                end = i
        
        while (start < end): # itera sobre esse espaço colocando as páginas no disco
            self.disk[start] = process.getId()
            start += 1
        
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
        
        self.removeFromDisk(process=process) # tiro o processo do disco para transferir à memória
        
        if self.freeSpace >= process.getPaginas(): # se tiver espaço suficiente, coloco direto, sem precisar do algoritmo
            
            # TODO: mudar essa lógica, pois dá erro quando tem espaço suficiente e o espaço não é contínuo, mas sim fragmentado entre a memória
            i = self.memory.index("-")
            last_page = i + process.getPaginas()
            while(i<last_page):
                self.memory[i] = process.getId()
                i+=1
            
            self.freeSpace -= process.getPaginas() # diminuo o contador de espaço livre na memória
            self.queue.append(process) # adiciono na fila de processos para o FIFO

        else:
            if self.algorithm == "FIFO":
                space_to_be_realocated = self.queue[0].getPaginas() # espaço que vou calcular se é suficiente para por o novo processo no lugar
                                
                while(space_to_be_realocated < process.getPaginas()): # se não for suficiente, vou dropar quantos processos forem necessários para caber o novo processo
                    self.reallocateInDisk(process=self.queue[0]) # realoco no disco o primeiro processo da fila
                    self.queue.popleft() # pop
                    
                    space_to_be_realocated += self.queue[0].getPaginas() # novo espaço para realocação
                    
                self.freeSpace += space_to_be_realocated # aumento o espaço o livre
                self.reallocateInDisk(process=self.queue[0]) # realoco o último processo necessário no disco
                    
                # acho o primeiro espaço livre após as realocações 
                # TODO: essa forma está errada de se fazer, preciso usar aquele método do achar o início e o fim
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



# -- TESTES --

p1 = Processo(0, 2, 3, 5, 1, 12)
p2 = Processo(1, 3, 5, 7, 2, 12)
p3 = Processo(2, 4, 6, 2, 3, 12)
p4 = Processo(3, 2, 2, 8, 4, 15)
    
all_processes_example = {
    p1: p1.getPaginas(),
    p2: p2.getPaginas(),
    p3: p3.getPaginas(),
    p4: p4.getPaginas()
}

a = Memory("FIFO", all_processes_example)

print(a.getDisk())
a.allocateInMemory(p1)
a.allocateInMemory(p2)
a.allocateInMemory(p3)
print(a.getMemory())
a.allocateInMemory(p4)
print(a.getMemory())
print(a.getDisk())
a.allocateInMemory(p1)
print(a.getMemory())
print(a.getDisk())

