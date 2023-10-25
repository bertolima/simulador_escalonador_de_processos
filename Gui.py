from tkinter import *
from tkinter import ttk
class Gui(Tk):
    def __init__(self):
        super().__init__()
        super().title("Escalonador de processos")
        self.value = None
        self.meters = None
        self.root = None
        self.feet = None
        self.test()

        #mainloop
        super().mainloop()
        
    def test(self):
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        super().columnconfigure(0, weight=1)
        super().rowconfigure(0, weight=1)

        self.feet = StringVar()
        self.feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        self.feet_entry.grid(column=2, row=1, sticky=(W, E))

        self.meters = StringVar()
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.feet_entry.focus()
        super().bind("<Return>", self.calculate)
    
    def calculate(self):
        try:
            self.value = float(self.feet.get())
            self.meters.set(int(0.3048 * self.value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
    
        

        