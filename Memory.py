from collections import deque
from Processo import *
class Memory:
    
    def __init__(self, algorithm, all_processes:dict): # dicionário {Processo: Nº Páginas}
        
        self.diskSize = 200
        self.disk = ["-"]*200
        
        self.pages = self.allocateAllPages(all_processes)
        
        self.memorySize = 50
        self.memory = ["-"]*50
        
        self.algorithm = algorithm
        self.freeSpace = self.memorySize
        self.queue = deque()
        
    def allocateAllPages(self, all_processes:dict): # dicionário {Processo: Nº Páginas}
        pages = 0
        
        for process in all_processes:
            process_pages = all_processes[process]
            for i in range(process_pages):
                self.disk[i + pages] = process.getId()
            
            pages += process_pages 
        
        return pages
        
    
    def reallocateInDisk(self):
        return
    
    def allocateInMemory(self, process:Processo):
        if process.getId() in self.memory:
            return
           
        if self.freeSpace > process.getPaginas():
            i = self.memory.index("-")
            last_page = i + process.getPaginas()
            while(i<last_page):
                self.memory[i] = process.getId()
                i+=1
            
            self.freeSpace -= process.getPaginas()
            self.queue.append(process)
            print(self.queue[0].getId())
        
                
    
    def getMemory(self):
        return self.memory
    
    def getDisk(self):
        return self.disk



p1 = Processo(0, 2, 3, 5, 1, 5)
p2 = Processo(1, 3, 5, 7, 2, 7)
p3 = Processo(2, 4, 6, 2, 3, 1)
p4 = Processo(3, 2, 2, 8, 4, 2)
    
all_processes_example = {
    p1: p1.getPaginas(),
    p2: p2.getPaginas(),
    p3: p3.getPaginas(),
    p4: p4.getPaginas()
}

a = Memory("FIFO", all_processes_example)

a.allocateInMemory(p1)
a.allocateInMemory(p2)
a.allocateInMemory(p3)
a.allocateInMemory(p4)

print(a.getDisk())

print(a.getMemory())


a.allocateInMemory(p2)

print(a.getMemory())