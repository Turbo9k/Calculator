import tkinter as tk
from tkinter import ttk, messagebox
import math

class AdvancedCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("750x650")  # Wider to accommodate history
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e1e')
        
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        self.current_input = ""
        self.result = None
        self.operation_pending = False
        self.history = []
        self.memory = 0
        self.angle_mode = "degrees"  # degrees or radians
        
        self.create_widgets()
        
    def configure_styles(self):
        # Configure button styles
        self.style.configure('Number.TButton',
                           background='#2d2d2d',
                           foreground='white',
                           font=('Arial', '12', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Operator.TButton',
                           background='#ff9500',
                           foreground='white',
                           font=('Arial', '12', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Function.TButton',
                           background='#505050',
                           foreground='white',
                           font=('Arial', '10', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Clear.TButton',
                           background='#ff3333',
                           foreground='white',
                           font=('Arial', '12', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Equals.TButton',
                           background='#ff9500',
                           foreground='white',
                           font=('Arial', '14', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Memory.TButton',
                           background='#9932cc',
                           foreground='white',
                           font=('Arial', '10', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Mode.TButton',
                           background='#008080',
                           foreground='white',
                           font=('Arial', '9', 'bold'),
                           borderwidth=1,
                           relief='flat')
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Advanced Calculator", 
                              font=('Arial', '18', 'bold'), 
                              bg='#1e1e1e', fg='white')
        title_label.pack(pady=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Left side - Calculator
        calc_frame = tk.Frame(main_frame, bg='#1e1e1e')
        calc_frame.pack(side='left', fill='both', expand=True)
        
        # Display
        display_frame = tk.Frame(calc_frame, bg='#1e1e1e')
        display_frame.pack(pady=(0,10), fill='x')
        
        self.display = tk.Entry(display_frame, textvariable=self.display_var,
                               font=('Arial', '20', 'bold'), 
                               justify='right', state='readonly',
                               bg='white', fg='black', 
                               relief='flat', bd=10)
        self.display.pack(fill='x', ipady=10)
        
        # Mode indicator
        mode_frame = tk.Frame(calc_frame, bg='#1e1e1e')
        mode_frame.pack(fill='x', pady=(0,5))
        
        self.mode_label = tk.Label(mode_frame, text=f"Mode: {self.angle_mode.title()}", 
                                  font=('Arial', '10'), 
                                  bg='#1e1e1e', fg='white')
        self.mode_label.pack(side='left')
        
        self.memory_label = tk.Label(mode_frame, text="M: 0", 
                                    font=('Arial', '10'), 
                                    bg='#1e1e1e', fg='white')
        self.memory_label.pack(side='right')
        
        # Button frame
        button_frame = tk.Frame(calc_frame, bg='#1e1e1e')
        button_frame.pack(fill='both', expand=True)
        
        # Create buttons
        self.create_buttons(button_frame)
        
        # Right side - History
        history_frame = tk.Frame(main_frame, bg='#2d2d2d', width=200)
        history_frame.pack(side='right', fill='y', padx=(10,0))
        history_frame.pack_propagate(False)
        
        # History title
        history_title = tk.Label(history_frame, text="History", 
                                font=('Arial', '14', 'bold'), 
                                bg='#2d2d2d', fg='white')
        history_title.pack(pady=10)
        
        # History listbox with scrollbar
        history_list_frame = tk.Frame(history_frame, bg='#2d2d2d')
        history_list_frame.pack(fill='both', expand=True, padx=10, pady=(0,10))
        
        scrollbar = tk.Scrollbar(history_list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_list_frame, 
                                         yscrollcommand=scrollbar.set,
                                         bg='#1e1e1e', fg='white',
                                         font=('Arial', '9'),
                                         selectbackground='#ff9500')
        self.history_listbox.pack(fill='both', expand=True)
        self.history_listbox.bind('<Double-Button-1>', self.recall_from_history)
        
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear history button
        clear_history_btn = ttk.Button(history_frame, text="Clear History", 
                                      style='Clear.TButton',
                                      command=self.clear_history)
        clear_history_btn.pack(pady=(0,10))
        
    def create_buttons(self, parent):
        # Button layout
        buttons = [
            # Row 1 - Memory and mode functions
            [('MC', 'Memory.TButton', self.memory_clear), ('MR', 'Memory.TButton', self.memory_recall), 
             ('M+', 'Memory.TButton', self.memory_add), ('M-', 'Memory.TButton', self.memory_subtract)],
            
            # Row 2 - Functions
            [('C', 'Clear.TButton', self.clear_all), ('CE', 'Clear.TButton', self.clear_entry), 
             ('±', 'Function.TButton', self.toggle_sign), ('√', 'Function.TButton', self.square_root)],
            
            # Row 3 - Trig functions
            [('sin', 'Function.TButton', self.sin), ('cos', 'Function.TButton', self.cos), 
             ('tan', 'Function.TButton', self.tan), ('DEG/RAD', 'Mode.TButton', self.toggle_angle_mode)],
            
            # Row 4 - Inverse trig functions
            [('asin', 'Function.TButton', self.asin), ('acos', 'Function.TButton', self.acos), 
             ('atan', 'Function.TButton', self.atan), ('π', 'Function.TButton', self.pi)],
            
            # Row 5 - Log functions and advanced
            [('log', 'Function.TButton', self.log10), ('ln', 'Function.TButton', self.ln), 
             ('x²', 'Function.TButton', self.square), ('xʸ', 'Function.TButton', self.power)],
            
            # Row 6 - More advanced functions
            [('x!', 'Function.TButton', self.factorial), ('e', 'Function.TButton', self.euler), 
             ('%', 'Function.TButton', self.percentage), ('1/x', 'Function.TButton', self.reciprocal)],
            
            # Row 7 - Numbers and operators
            [('7', 'Number.TButton', lambda: self.number_input('7')), 
             ('8', 'Number.TButton', lambda: self.number_input('8')), 
             ('9', 'Number.TButton', lambda: self.number_input('9')), 
             ('÷', 'Operator.TButton', lambda: self.operator_input('/'))],
            
            # Row 8
            [('4', 'Number.TButton', lambda: self.number_input('4')), 
             ('5', 'Number.TButton', lambda: self.number_input('5')), 
             ('6', 'Number.TButton', lambda: self.number_input('6')), 
             ('×', 'Operator.TButton', lambda: self.operator_input('*'))],
            
            # Row 9
            [('1', 'Number.TButton', lambda: self.number_input('1')), 
             ('2', 'Number.TButton', lambda: self.number_input('2')), 
             ('3', 'Number.TButton', lambda: self.number_input('3')), 
             ('-', 'Operator.TButton', lambda: self.operator_input('-'))],
            
            # Row 10
            [('0', 'Number.TButton', lambda: self.number_input('0')), 
             ('.', 'Number.TButton', lambda: self.number_input('.')), 
             ('Ans', 'Function.TButton', self.recall_answer), 
             ('+', 'Operator.TButton', lambda: self.operator_input('+'))],
            
            # Row 11 - Equals button spanning 4 columns
            [('=', 'Equals.TButton', self.calculate, 4)]
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, button_info in enumerate(row):
                if len(button_info) == 4:  # Equals button with colspan
                    text, style, command, colspan = button_info
                    btn = ttk.Button(parent, text=text, style=style, command=command)
                    btn.grid(row=row_idx, column=0, columnspan=colspan, 
                            sticky='nsew', padx=2, pady=2)
                else:
                    text, style, command = button_info
                    btn = ttk.Button(parent, text=text, style=style, command=command)
                    btn.grid(row=row_idx, column=col_idx, 
                            sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights
        for i in range(11):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
    
    def update_display(self, value):
        self.display_var.set(str(value))
    
    def number_input(self, num):
        if self.operation_pending:
            self.current_input = ""
            self.operation_pending = False
        
        if self.current_input == "0" and num != ".":
            self.current_input = num
        else:
            self.current_input += num
        
        self.update_display(self.current_input)
    
    def operator_input(self, op):
        try:
            if self.current_input:
                self.result = float(self.current_input)
            self.operator = op
            self.operation_pending = True
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
    
    def calculate(self):
        try:
            if hasattr(self, 'operator') and self.current_input:
                current_num = float(self.current_input)
                
                # Store calculation for history
                if self.operator == '+':
                    result = self.result + current_num
                    calculation = f"{self.result} + {current_num} = {result}"
                elif self.operator == '-':
                    result = self.result - current_num
                    calculation = f"{self.result} - {current_num} = {result}"
                elif self.operator == '*':
                    result = self.result * current_num
                    calculation = f"{self.result} × {current_num} = {result}"
                elif self.operator == '/':
                    if current_num == 0:
                        messagebox.showerror("Error", "Division by zero!")
                        return
                    result = self.result / current_num
                    calculation = f"{self.result} ÷ {current_num} = {result}"
                elif self.operator == '**':
                    result = self.result ** current_num
                    calculation = f"{self.result}^{current_num} = {result}"
                
                # Add to history
                self.add_to_history(calculation)
                
                self.current_input = str(result)
                self.update_display(result)
                self.result = result
                self.last_result = result  # Store for Ans button
                
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def clear_all(self):
        self.current_input = "0"
        self.result = None
        self.operation_pending = False
        if hasattr(self, 'operator'):
            delattr(self, 'operator')
        self.update_display("0")
    
    def clear_entry(self):
        self.current_input = "0"
        self.update_display("0")
    
    def toggle_sign(self):
        try:
            if self.current_input and self.current_input != "0":
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.update_display(self.current_input)
        except:
            pass
    
    def square_root(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            if num < 0:
                messagebox.showerror("Error", "Cannot calculate square root of negative number!")
                return
            result = math.sqrt(num)
            calculation = f"√{num} = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def square(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            result = num ** 2
            calculation = f"{num}² = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def power(self):
        try:
            if self.current_input:
                self.result = float(self.current_input)
            self.operator = '**'
            self.operation_pending = True
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
    
    def sin(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            angle = math.radians(num) if self.angle_mode == "degrees" else num
            result = math.sin(angle)
            calculation = f"sin({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def cos(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            angle = math.radians(num) if self.angle_mode == "degrees" else num
            result = math.cos(angle)
            calculation = f"cos({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def tan(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            angle = math.radians(num) if self.angle_mode == "degrees" else num
            result = math.tan(angle)
            calculation = f"tan({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def log10(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            if num <= 0:
                messagebox.showerror("Error", "Number must be positive for logarithm!")
                return
            result = math.log10(num)
            calculation = f"log({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def ln(self):
        try:
            num = float(self.current_input) if self.current_input else 0
            if num <= 0:
                messagebox.showerror("Error", "Number must be positive for natural logarithm!")
                return
            result = math.log(num)
            calculation = f"ln({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def pi(self):
        self.current_input = str(math.pi)
        self.update_display(math.pi)
    
    def euler(self):
        self.current_input = str(math.e)
        self.update_display(math.e)
    
    # New advanced functions
    def add_to_history(self, calculation):
        """Add calculation to history"""
        self.history.append(calculation)
        self.history_listbox.insert(tk.END, calculation)
        self.history_listbox.see(tk.END)  # Auto-scroll to bottom
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
    
    def recall_from_history(self, event):
        """Recall calculation from history by double-clicking"""
        selection = self.history_listbox.curselection()
        if selection:
            calculation = self.history_listbox.get(selection[0])
            # Extract result from calculation (after '=' sign)
            if '=' in calculation:
                result = calculation.split('=')[-1].strip()
                self.current_input = result
                self.update_display(result)
    
    def toggle_angle_mode(self):
        """Toggle between degrees and radians"""
        self.angle_mode = "radians" if self.angle_mode == "degrees" else "degrees"
        self.mode_label.config(text=f"Mode: {self.angle_mode.title()}")
    
    def update_memory_display(self):
        """Update memory display"""
        self.memory_label.config(text=f"M: {self.memory}")
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.update_memory_display()
    
    def memory_recall(self):
        """Recall value from memory"""
        self.current_input = str(self.memory)
        self.update_display(self.memory)
    
    def memory_add(self):
        """Add current value to memory"""
        try:
            current_val = float(self.current_input) if self.current_input else 0
            self.memory += current_val
            self.update_memory_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for memory operation!")
    
    def memory_subtract(self):
        """Subtract current value from memory"""
        try:
            current_val = float(self.current_input) if self.current_input else 0
            self.memory -= current_val
            self.update_memory_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for memory operation!")
    
    def factorial(self):
        """Calculate factorial"""
        try:
            num = float(self.current_input) if self.current_input else 0
            if num < 0 or num != int(num):
                messagebox.showerror("Error", "Factorial requires a non-negative integer!")
                return
            result = math.factorial(int(num))
            calculation = f"{int(num)}! = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def percentage(self):
        """Calculate percentage (divide by 100)"""
        try:
            num = float(self.current_input) if self.current_input else 0
            result = num / 100
            calculation = f"{num}% = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def reciprocal(self):
        """Calculate reciprocal (1/x)"""
        try:
            num = float(self.current_input) if self.current_input else 0
            if num == 0:
                messagebox.showerror("Error", "Cannot calculate reciprocal of zero!")
                return
            result = 1 / num
            calculation = f"1/{num} = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def asin(self):
        """Calculate arcsine"""
        try:
            num = float(self.current_input) if self.current_input else 0
            if abs(num) > 1:
                messagebox.showerror("Error", "Input must be between -1 and 1 for arcsine!")
                return
            result_rad = math.asin(num)
            result = math.degrees(result_rad) if self.angle_mode == "degrees" else result_rad
            calculation = f"asin({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def acos(self):
        """Calculate arccosine"""
        try:
            num = float(self.current_input) if self.current_input else 0
            if abs(num) > 1:
                messagebox.showerror("Error", "Input must be between -1 and 1 for arccosine!")
                return
            result_rad = math.acos(num)
            result = math.degrees(result_rad) if self.angle_mode == "degrees" else result_rad
            calculation = f"acos({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def atan(self):
        """Calculate arctangent"""
        try:
            num = float(self.current_input) if self.current_input else 0
            result_rad = math.atan(num)
            result = math.degrees(result_rad) if self.angle_mode == "degrees" else result_rad
            calculation = f"atan({num}) = {result}"
            self.add_to_history(calculation)
            self.current_input = str(result)
            self.update_display(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def recall_answer(self):
        """Recall last calculated result"""
        if hasattr(self, 'last_result'):
            self.current_input = str(self.last_result)
            self.update_display(self.last_result)
        else:
            messagebox.showinfo("Info", "No previous answer to recall!")

def main():
    root = tk.Tk()
    app = AdvancedCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 