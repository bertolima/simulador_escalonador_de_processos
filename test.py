import tkinter as tk

class Example():

 def render_gui(self):

    self.main_window = tk.Tk()
    self.main_window.geometry("1000x600")
    self.main_window.title("Damaged Text Document Virtual Restoration")
    self.main_window.resizable(True, True) 
    self.main_window.configure(background="#d9d9d9")
    self.main_window.configure(highlightbackground="#d9d9d9")
    self.main_window.configure(highlightcolor="black")

    canvas_container = tk.Frame(self.main_window, bd=1, relief='sunken')
    canvas_container.pack(expand = True, fill = "both")

    self.main_canvas = tk.Canvas(canvas_container, bg = "yellow")
    vsb = tk.Scrollbar(canvas_container, orient="vertical", command=self.main_canvas.yview)
    hsb = tk.Scrollbar(canvas_container, orient="horizontal", command=self.main_canvas.xview)
    self.main_canvas.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)

    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    self.main_canvas.grid(row=0, column=0, sticky="nsew")
    canvas_container.grid_rowconfigure(0, weight=1)
    canvas_container.grid_columnconfigure(0, weight=1)

    self.main_window.mainloop()

e = Example()
e.render_gui()