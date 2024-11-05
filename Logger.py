import tkinter as tk

class Logger:
    def __init__(self, root: tk.Tk) -> None:
        self.window: tk.Tk = root
        self.frame: tk.Frame = tk.Frame(self.window, width=45, height=28, background="#606060", relief='raised')
        self.frame.grid(row=11, column=1, padx=(0, 10), rowspan=4, pady=(0, 5), sticky="e")
        
        self.container: tk.Label = tk.Label(self.frame, width=45, height=28, background="#232324", bd=2)
        self.container.grid(row=0, column=0, padx=(3, 0), sticky="nswe")
        
        self.draw_text_area()
    
    def draw_text_area(self) -> None:
        self.text_area: tk.Text = tk.Text(self.container, width=22, height=6)
        self.text_area.grid(row=0, column=1, rowspan=3, padx=(0, 2), sticky="nw")

        self.scrollbar: tk.Scrollbar = tk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.text_area.yview)
        self.scrollbar.grid(row=0, column=4, rowspan=3, pady=(0, 0), sticky="ns")

        self.text_area.config(relief='solid', bg='#232324', fg='white', bd=0, yscrollcommand=self.scrollbar.set)
        self.text_area.config(state='disabled', wrap=tk.WORD)
     
    def log(self, log_msg: str, color: str = "white") -> None:
        tag_name: str = f"color_{color}"
        self.text_area.tag_config(tag_name, foreground=color)
        
        self.text_area.config(state='normal')
        self.text_area.insert('end', log_msg + '\n', tag_name)
        self.text_area.see('end')
        self.text_area.config(state='disabled')
        
        self.window.update()