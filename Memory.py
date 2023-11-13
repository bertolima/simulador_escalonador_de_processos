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
        
    
    def reallocateInDisk(self, process:Processo):
        i = self.memory.index(process.getId())
        last_page = i + process.getPaginas()
        
        while (i < last_page):
            self.memory[i] = "-"
            i+=1
        
        start = 0
        end = 0
        for i in range(self.diskSize):
            if (end - start) == process.getPaginas():
                break
            
            if self.disk[i] == "-":
                end += 1
            else:
                start = i
                end = i
        
        while (start < end):
            self.disk[start] = process.getId()
            start += 1
        
    def removeFromDisk(self, process:Processo):
        i = self.disk.index(process.getId())
        last_page = i + process.getPaginas()
        
        while (i < last_page):
            self.disk[i] = "-"
            i+=1
    
    def allocateInMemory(self, process:Processo):
        if process.getId() in self.memory:
            return
              
        self.removeFromDisk(process=process)
        
        if self.freeSpace >= process.getPaginas():
            # TODO: mudar essa lógica, pois dá erro quando tem espaço suficiente e o espaço não é contínuo, mas sim fragmentado entre a memória
            i = self.memory.index("-")
            last_page = i + process.getPaginas()
            while(i<last_page):
                self.memory[i] = process.getId()
                i+=1
            
            self.freeSpace -= process.getPaginas()
            self.queue.append(process)

        else:
            if self.algorithm == "FIFO":
                space_to_be_realocated = self.queue[0].getPaginas()
                                
                while(space_to_be_realocated < process.getPaginas()):
                    self.reallocateInDisk(process=self.queue[0])
                    self.queue.popleft()
                    
                    space_to_be_realocated += self.queue[0].getPaginas()
                    
                self.freeSpace += space_to_be_realocated
                self.reallocateInDisk(process=self.queue[0])
                    

                i = self.memory.index("-")
                last_page = i + process.getPaginas()
                
                while(i<last_page):
                    self.memory[i] = process.getId()
                    i+=1
                
                
                self.freeSpace -= process.getPaginas()
                self.queue.append(process)
        
                    
                           
    
    def getMemory(self):
        return self.memory
    
    def getDisk(self):
        return self.disk



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

