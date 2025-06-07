import tkinter as tk
from tkinter import font
import math

class AnimatedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = self['bg']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<ButtonPress-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        
    def on_enter(self, e):
        self['bg'] = self['activebackground']
        
    def on_leave(self, e):
        self['bg'] = self.default_bg
        
    def on_press(self, e):
        self['relief'] = tk.SUNKEN
        
    def on_release(self, e):
        self['relief'] = tk.RAISED
        self['bg'] = self['activebackground']

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Modern Calculator")
        master.geometry("300x450")
        master.resizable(False, False)
        master.configure(bg='#111')
        
        # Custom font
        self.button_font = font.Font(family='Helvetica', size=12, weight='bold')
        self.display_font = font.Font(family='Helvetica', size=20)
        
        # Colors
        self.display_bg = '#ff8600'
        self.number_bg = '#e0e0e0'
        self.operator_bg = '#ff9500'
        self.special_bg = '#ff9500'
        self.text_color = '#111'
        self.operator_text = '#fff'
        
        # Create display
        self.display_var = tk.StringVar()
        self.display = tk.Entry(master, textvariable=self.display_var, 
                               font=self.display_font, bg=self.display_bg,
                               borderwidth=0, relief=tk.FLAT, justify='right',
                               insertwidth=0, highlightthickness=2, 
                               highlightbackground='#1bc', highlightcolor='#007aff')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=15, sticky='nsew')
        
        # Button layout
        buttons = [
            ('C', 1, 0, self.special_bg), ('√', 1, 1, self.special_bg), ('^', 1, 2, self.special_bg), ('/', 1, 3, self.operator_bg),
            ('7', 2, 0, self.number_bg), ('8', 2, 1, self.number_bg), ('9', 2, 2, self.number_bg), ('*', 2, 3, self.operator_bg),
            ('4', 3, 0, self.number_bg), ('5', 3, 1, self.number_bg), ('6', 3, 2, self.number_bg), ('-', 3, 3, self.operator_bg),
            ('1', 4, 0, self.number_bg), ('2', 4, 1, self.number_bg), ('3', 4, 2, self.number_bg), ('+', 4, 3, self.operator_bg),
            ('0', 5, 0, self.number_bg), ('.', 5, 1, self.number_bg), ('⌫', 5, 2, self.special_bg), ('=', 5, 3, self.operator_bg)
        ]
        
        # Configure grid
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        
        # Create buttons with animations
        for (text, row, col, bg) in buttons:
            active_bg = self.lighten_color(bg, 20)
            fg = self.operator_text if bg == self.operator_bg else self.text_color
            
            btn = AnimatedButton(
                master, text=text, font=self.button_font,
                bg=bg, activebackground=active_bg, fg=fg,
                borderwidth=0, relief=tk.RAISED,
                command=lambda t=text: self.handle_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            btn.config(highlightbackground='#cccccc', highlightthickness=1)
        
        # Initialize calculator state
        self.current_input = ''
        self.reset_on_next_input = False
    
    def lighten_color(self, color, percent):
        """Lighten a color by a percentage"""
        # This is a simplified color lightening function
        # For a real app, you'd want a more sophisticated color manipulation
        return color  # In a real implementation, this would lighten the color
    
    def handle_click(self, value):
        current = self.display_var.get()
        
        if self.reset_on_next_input and value not in '+-*/^':
            self.current_input = ''
            self.reset_on_next_input = False
        
        if value == 'C':
            self.current_input = ''
            self.display_var.set('')
        elif value == '⌫':
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input)
        elif value == '=':
            try:
                result = eval(self.current_input)
                self.display_var.set(result)
                self.current_input = str(result)
                self.reset_on_next_input = True
            except:
                self.display_var.set("Error")
                self.current_input = ''
        elif value == '√':
            try:
                result = math.sqrt(float(current))
                self.display_var.set(result)
                self.current_input = str(result)
                self.reset_on_next_input = True
            except:
                self.display_var.set("Error")
                self.current_input = ''
        elif value == '^':
            self.current_input += '**'
            self.display_var.set(self.current_input)
        else:
            self.current_input += value
            self.display_var.set(self.current_input)

# Create the main window
root = tk.Tk()
calculator = Calculator(root)
root.mainloop()