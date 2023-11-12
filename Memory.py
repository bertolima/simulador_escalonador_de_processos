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
        
    def allocateAllPages(self, all_processes:dict):
        pages = 0
        
        for process in all_processes:
            process_pages = all_processes[process]
            for i in range(process_pages):
                self.disk[i + pages] = process.getId()
            
            pages += process_pages 
        
        return pages
        
    
    def allocateInDisk(self):
        return
    
    def allocateInMemory(self):
        return
    
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

a = Memory("Fifo", all_processes_example)

print(a.getDisk())