import tkinter as tk
import sqlite3


conn = sqlite3.connect('calculator.db')
c = conn.cursor()

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Calculator')
        self.input_field = tk.Entry(master, width=30)
        self.input_field.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.create_buttons()

    def create_buttons(self):
   
        button_labels = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+']
        button_functions = [self.add_to_input, self.add_to_input, self.add_to_input, self.add_to_input,
                            self.add_to_input, self.add_to_input, self.add_to_input, self.add_to_input,
                            self.add_to_input, self.add_to_input, self.add_to_input, self.add_to_input,
                            self.add_to_input, self.add_to_input, self.calculate, self.add_to_input]

   
        row, col = 1, 0
        for label, function in zip(button_labels, button_functions):
            if label == '=':
                button = tk.Button(self.master, text=label, width=7, height=2, command=function)
                button.grid(row=row, column=col, rowspan=2, padx=5, pady=5)
            else:
                button = tk.Button(self.master, text=label, width=7, height=2, command=function)
                button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def add_to_input(self):
  
        button_label = self.master.focus_get()['text']
        current_input = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, current_input + button_label)

    def calculate(self):
        
        expression = self.input_field.get()
        try:
            result = eval(expression)
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, result)
           
            c.execute('INSERT INTO calculations (expression, result) VALUES (?, ?)', (expression, result))
            conn.commit()
        except:
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, 'Error')


c.execute('''CREATE TABLE IF NOT EXISTS calculations
             (expression text, result real)''')


root = tk.Tk()
app = CalculatorGUI(root)
root.mainloop()


conn.close()
