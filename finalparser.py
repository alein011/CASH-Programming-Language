import re
from new_function import *
from plot import *
from lexer import Lexer

"""
The code represents a simple programming language with a focus on financial calculations.
It includes functionality for variable assignments, basic mathematical operations, conditionals (if, else),
loops (for, while), function definitions, and function calls. Additionally, it supports input/output
operations for user interaction and displays the results.

Key components:
- `Tables_Values` class maintains variables, functions, and output storage.
- `Parser` class processes the input code, executes statements, and handles errors.
- Financial functions are defined and mapped to execute based on keywords.
- Display, input, and control flow statements are implemented.
- Lexer converts the input script into tokens.

Example usage is provided at the end of the code, where a sample input code is tokenized and displayed.

Note: Before running this code, make sure to download the required modules such as matplotlib, prettytable, and numpy
"""

class Tables_Values:
    def __init__(self):
        self.variables = {}     # List of variables
        self.function = {}      # List of function names
        self.terminal = ""      # stores all the output
        self.output = ""        # stores all the value from functions

    # to access the value of a variable
    def get_variable(self, var_name):
        return self.variables.get(var_name, None)

    # assigns value to the variable
    def set_variable(self, var_name, value):
        self.variables[var_name] = value
        
    # return all the output of functions    
    def get_terminal(self):
        return self.terminal
    def __repr__(self):
        return self.terminal


# handles error in the syntax
class Error:
    def __init__(self, message, lineno):
        self.message = message
        self.lineno = lineno
        
    def __repr__(self) -> str:
        return f"Error in line {self.lineno}: {self.message}"
    
def get(prompt):   
    return input(prompt)


# to catch invalid format for string and identifier
IDENTIFIER = r'\b(_*[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)*)+\b'
STRING = r'(\"([^"\n]*)\")|(\'([^"\n]*)\')'    
        
        
class Parser:
    def __init__(self, table_values):
        self.table_values = table_values        
        self.code = []                      # list of the code per line
        self.line_number = 0                # tracks line number
        self.output = []                    # stores the output of the function
        self.result = []
        
    def parse_code(self, code):
        self.table_values.variables.clear()
        self.table_values.variables.update(globals())
        self.code = code
        self.run_code()

    def run_code(self):
        try:
            while self.line_number < len(self.code):
                self.execute_line()
            #return(self.table_values.terminal)
        except Exception as e:
            print(f"Error in line {self.line_number + 1}: {str(e)}")
        
    # adds error to the result       
    def add_error(self, error_message):
        error_message += '\n'
        self.output += error_message 
        self.table_values.terminal += str(error_message) 



    # to map which bmath function to run
    financial_function_mapping = {
        "simple_interest": "execute_sint",
        "compound_interest": "execute_cint",
        "simple_annuity": "execute_sann",
        "stock_dividend": "execute_stock_div",
        "div_pershare": "execute_dps",
        "yield_ratio": "execute_yr",
        "coupon_payment": "execute_cp",
        "coupon_amount": "execute_ca",
        "loan_principal": "execute_loanp",
        "loanfv_pin": "execute_lfv_pin",
        "loanfv_rtm": "execute_lfv_rtm",
    }
    


    # maps the code to identify which function to perform
    def execute_line(self):
        line = self.code[self.line_number].strip()
    
        # skips empty line      
        if not line:
            self.line_number += 1 
            return
        
        # handles comment
        if line.startswith('##'):
            self.line_number += 1
            while self.line_number < len(self.code) and not line.endswith('##') and not line.startswith('##'):
                self.line_number += 1
                
                if line.endswith('##') or line.startswith('##'):
                    self.line_number += 1
                    continue
            else:
                print(f"Error in line {self.line_number + 1}") 
        elif line.startswith('#'):
            self.line_number += 1
            return
        
        # other CASH functions
        elif line.startswith("display("):
            self.execute_display(line)
        elif line.startswith("get("):
            self.execute_get(line)
        elif line.startswith("if "):
            self.execute_if(line)
        elif line.startswith("for "):
            self.execute_for(line)
        elif line.startswith("while "):
            self.execute_while(line)
        elif re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*([+\-*\/%]?=|\+\+|--)\s*(.*?)\s*$', line):
            self.execute_assignment(line)   
        elif line.startswith("func ") or line.startswith("function "):
            self.create_function(line)
        else:
            # maps the functions called
            for prefix, method in self.financial_function_mapping.items():
                if line.startswith(f"{prefix}("):
                    getattr(self, method)(line)
                    break
            else:
                if line.endswith(")") and "(" in line:
                    try:
                        self.execute_function_call(line)
                    except Exception as e:
                        print(f"Error in line {self.line_number + 1}: {str(e)}")
            
        # incr to move to the new line    
        self.line_number += 1
    
    
    
    # functions to execute bmath without the rw display
    def execute_financial_function(self, line):
        error_message = ''
        try:
            if not line.endswith(")"):
                raise SyntaxError(Error("Expected ')'", self.line_number + 1))
            result = eval(line, self.table_values.variables)
            print(result)
            y = str(result) + '\n'
            #self.table_values.add_data(y)
            self.table_values.terminal += y
            self.output += y
        
        except SyntaxError as se:
            error_message = str(f"{se}")
        except Exception as e:
           error_message = (f"Error in line {self.line_number + 1}: {e}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)    
    
    def execute_sint(self, line):
        self.execute_financial_function(line)
        
    def execute_cint(self, line):
        self.execute_financial_function(line)
        
    def execute_sann(self, line):
        self.execute_financial_function(line)

    def execute_stock_div(self, line):
        self.execute_financial_function(line)

    def execute_dps(self, line):
        self.execute_financial_function(line)

    def execute_yr(self, line):
        self.execute_financial_function(line)

    def execute_cp(self, line):
        self.execute_financial_function(line)

    def execute_ca(self, line):
        self.execute_financial_function(line)

    def execute_loanp(self, line):
        self.execute_financial_function(line)

    def execute_lfv_pin(self, line):
        self.execute_financial_function(line)

    def execute_lfv_rtm(self, line):
        self.execute_financial_function(line)


    #handles display statement
    def execute_display(self, line):
        error_message = ''
        try: 
            if not line.endswith(")"):
                raise SyntaxError(Error("Expected ')'", self.line_number + 1))
            expression = line[8:-1].strip()
            result = eval(expression, self.table_values.variables)
            print(result)
            self.output.append(result)
            y = str(result) + '\n'
            self.table_values.terminal += y 
        except SyntaxError as se:
            error_message = str(Error("Invalid syntax. Check for missing operators or unterminated string literal", self.line_number + 1))
        except Exception as e:
           error_message = (f"Error in line {self.line_number + 1}: {e}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)


    # handles get statement
    def execute_get(self, line):
        error_message = ''
        try:
            if not line.endswith(")"):
                raise SyntaxError(Error("Expected ')'", self.line_number + 1))
            prompt = line[4:-1]
            user_input = get(prompt)
            self.table_values.set_variable(prompt, user_input)
            self.output.append(user_input)
            y = str(user_input) + '\n'
            self.table_values.terminal += y 
            
        except SyntaxError as se:
            error_message = str(se)
        except Exception as e:
           error_message = (f"Error in line {self.line_number + 1}: {e}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

    
    # handles assignment statement
    def execute_assignment(self, line):
        error_message = ''
        pattern = r'(\b(\w+)\b\s*([+\-*/]?=|^|\*\*|\+\+[\+]?|--[-]?)\s*("[^"]*"|\d+|\'[^\']*\'|(\S+\s*)*)\s*)'
        matches = re.findall(pattern, line)
        #print(matches)
        for match in matches:
            var_name, op, expression = match[1], match[2], match[3]
        valid = True
        try:
            
            # handles invalid identifier
            if re.search(IDENTIFIER, var_name):
                pass
            else:
                raise SyntaxError(Error(f"Invalid identifier '{var_name}'", self.line_number + 1))
                
            # handles too much operator
            if len(op) > 2:
                valid = False
                       
            if op == '=':
                    try:
                        value = eval(expression, self.table_values.variables)
                        self.table_values.set_variable(var_name, value)
                        
                    except Exception:
                        raise Exception(Error(f"Invalid syntax", self.line_number+1))
            else: 
                current_value = self.table_values.get_variable(var_name)
                if expression:
                    new_value = eval(expression, self.table_values.variables)

                if op == '':
                    self.table_values.set_variable(var_name, new_value)
                elif op == '+=':
                    self.table_values.set_variable(var_name, current_value + new_value)
                elif op == '-=':
                    self.table_values.set_variable(var_name, current_value - new_value)
                elif op == '*=':
                    self.table_values.set_variable(var_name, current_value * new_value)
                elif op == '/=':
                    self.table_values.set_variable(var_name, current_value / new_value)
                elif op == '%=':
                    self.table_values.set_variable(var_name, current_value % new_value)
                
                if op == '++':
                    self.table_values.set_variable(var_name, current_value + 1)
                elif op == '--':
                    self.table_values.set_variable(var_name, current_value - 1)
                elif valid == False:
                    raise SyntaxError(f"Error in line {self.line_number + 1}: Invalid syntax '{op}'")
                else:
                    raise SyntaxError(f"Error in line {self.line_number + 1}: Invalid syntax '{op}'")
        
        except SyntaxError as se:
            error_message = str(se)
            
        except Exception as e:
            error_message = (f"{e}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)
     
     
    # handles while statement      
    def execute_while(self, line):
        error_message = ''
        try:
            if not line.endswith(':'):
                raise SyntaxError(Error("Expected ':'", self.line_number+ 1))
            condition = line[6:-1].strip()
            saved_row = self.line_number
            identifier = r'^[a-zA-Z_][a-zA-Z0-9_]*'
            value = self.table_values.get_variable(identifier)
            cond = eval(condition, self.table_values.variables)
            if cond == False:
                self.skip_block(line)
        
            while cond:
                self.line_number += 1
                while (
                    self.line_number < len(self.code)
                    and self.get_indent_level(self.code[self.line_number]) > self.get_indent_level(line)
                ):
                    self.execute_line()
                self.line_number -= 1
                
                # Update the condition for the next iteration
                cond = eval(condition, self.table_values.variables)
                if cond:  
                    self.line_number = saved_row
                    
        except SyntaxError as se:
            error_message = str(se)
            
        except Exception as e:
            print(f"Error in line {self.line_number + 1}: {e}")
                
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)      
        
    def skip_block(self, line):
        error_message = ''
        try:
            level = 1
            inside_else = False  # Flag to track if currently inside an 'else' block
            # while level > 0:
            while self.line_number + 1 < len(self.code) and self.get_indent_level(self.code[self.line_number + 1]) > self.get_indent_level(line):
                self.skip_line()
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

    
    # handles if statement
    def execute_if(self, line):
        error_message = ''
        try:
            if not line.endswith(':'):
                raise SyntaxError(Error("Expected ':'", self.line_number+ 1))
            condition = line[3:-1].strip()
            if eval(condition, self.table_values.variables):
                self.execute_block(line)
            else:
                self.execute_else(line)
        except SyntaxError as se:
            error_message = str(se)
            
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")
            
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

    def execute_block(self, line):
        error_message = ''
        try:   
            self.line_number += 1
            while self.get_indent_level(self.code[self.line_number]) > self.get_indent_level(line) and not self.code[self.line_number].strip().startswith("else"):
                self.execute_line()

            if self.line_number < len(self.code) and self.code[self.line_number].strip().startswith("else:"):
                while self.get_indent_level(self.code[self.line_number + 1]) > self.get_indent_level(line):
                    self.skip_line()
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")

        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)
            
    def execute_else(self, line):
        error_message = ''
        try:
            level = 1
            inside_else = False
            while self.line_number + 1 < len(self.code) and self.get_indent_level(self.code[self.line_number + 1]) > self.get_indent_level(line):
                self.skip_line()
            self.line_number += 1
            if self.line_number < len(self.code) and self.code[self.line_number].strip().startswith("else:"):
                while self.get_indent_level(self.code[self.line_number + 1]) > self.get_indent_level(line) and not self.code[self.line_number].strip().startswith("else"):
                    self.execute_line()
            else:
                self.execute_line()
                self.line_number -= 1
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")

        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)
    
    
    # handles creation and calling of function
    def create_function(self, line):
        error_message = ''
        # Parse the function definition
        try:
            match = re.match(r'(func|function)\s+([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)\s*:', line)

            keyword, func_name, params_str = match.groups()
            params = [param.strip() for param in params_str.split(',')]

            # Parse the function body
            function_body = []
            self.line_number += 1
            while self.line_number < len(self.code) and not self.code[self.line_number].strip().endswith(':'):
                function_body.append(self.code[self.line_number])
                self.line_number += 1
                
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")

        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

        # Create the function
        function_code = '\n'.join(function_body)
        function_code = function_code.replace('\t', ' ' * 4)  # Replace tabs with spaces for consistent indentation
        function_code = f"def {func_name}({', '.join(params)}):\n    {function_code}"
        
        error_message = ''
        # Execute the function code
        try:
            exec(function_code, self.table_values.variables)
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: {str(e)}")

        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

    def execute_function_call(self, line):
        error_message = ''
        try:
            result = eval(line, self.table_values.variables)
            self.output.append(result)
            y = str(result) + '\n'
        except Exception as e:
            error_message = (f"Error in line {self.line_number + 1}: Function name does not exist")
        
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)
             
    
    # handles for statement
    def execute_for(self, line):
        error_message = ''
        
        try:
            line = line.strip('for')
            if not line.endswith(':'):
                raise SyntaxError(Error("Expected ':'", self.line_number+ 1))
            line = line.rstrip(':')
            identifier, range_part = line.split("in")
            identifier = identifier.replace(" ", "")
            rangelist = list(eval(range_part))
            saved_row = self.line_number
            
            if re.search(IDENTIFIER, identifier):
                pass
            else:
                raise SyntaxError(Error(f"Invalid identifier '{identifier}'", self.line_number + 1))

            for value in rangelist:
                self.table_values.set_variable(identifier, value)
                
                while self.line_number + 1 < len(self.code) and self.get_indent_level(self.code[self.line_number + 1]) > self.get_indent_level(line):
                    self.line_number += 1
                    self.execute_line()
                self.line_number = saved_row
            
            self.line_number += 1

        except SyntaxError as se:
            error_message = str(se)
            
        except Exception as e:
            error_message = f"Error in line {self.line_number + 1}: for statement should have a valid identifier and range list"
        
        if error_message:
            print(f"{error_message}")
            self.add_error(error_message)

    def skip_line(self):
        self.line_number += 1
    
    # checks the proper indentation
    def get_indent_level(self, line):
        return len(line) - len(line.lstrip())
    

# calls the lexer functions    
def lexer(data):
    table_values = Tables_Values()
    parser = Parser(table_values)
    lexer = Lexer(data)
    
    #lexeme = lexer.run(data)
    
    tokens = lexer.pass_data()
    res = parser.parse_code(tokens)
    result = table_values.get_terminal()
    return result

  

    
  


