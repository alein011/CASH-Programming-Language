from datetime import datetime
import re
from prettytable import *

"""
This script defines a lexer for CASH programming language. It tokenizes input code into a list of tokens, where each token 
has a type(token), lexeme, line number, starting index, ending index, and optional error message.

The lexer recognizes various operators, keywords, reserved words, and identifiers. It also handles integer and floating-point 
literals, strings, and comments (both single-line and multi-line).

To use the lexer:
1. Create an instance of the Lexer class with the input code.
2. Call the `tokenize` method to obtain a list of Token objects.
3. Optionally, you can run the `run` function to display the tokenized information in a pretty table and save it to a file.

Example usage is provided at the end of the script, where a sample input code is tokenized and displayed.

Note: Before running this script, make sure to download the required modules.
"""


# List of lexemes and tokens
operator_deli = {
    '+=': 'ADD_EQUAL',
    '-=': 'SUB_EQUAL',
    '=': 'DIV_EQUAL',
    '%=': 'MOD_EQUAL',
    '++': 'INCR_OP',
    '--': 'DECR_OP',
    '+': 'ADD_OP',
    '-': 'SUB_OP',
    '*': 'MUL_OP',
    '/': 'DIV_OP',
    '%': 'MOD_OP',
    '^': 'EXP_OP',
    '==': 'EQTO_OP',
    '=': 'EQUAL_OP',
    '<=': 'LTEQ_TO',
    '<': 'LT_OP',
    '>=': 'GTEQ_TO',
    '>': 'GT_OP',
    '!=': 'NOTEQ_OP',
    '##[\s\S]*##': 'MULT_COM',
    '^#(.*)$': 'SINGLE_COM',
    '(': 'LPAREN_DEL',
    ')': 'RPAREN_DEL',
    '{': 'LCURLY_DEL',
    '}': 'RCURLY_DEL',
    '[': 'LSQUARE_DEL',
    ']': 'RSQUARE_DEL',
    ':': 'COLON_DEL',
    ';': 'SEMICOLON_DEL',
    ',': 'COMMA_DEL',
    '|': 'OR_OP',
    '!': 'NOT_OP',
    '&': 'AND_OP',
    '+++': 'INVALID_TOKEN'
    }

keywords = {
    'true': 'TRUE_KW',
    'false': 'FALSE_KW',
    'none': 'NONE_RW'
}

reserved_words = {
    'func': 'FUNCTION_RW',
    'function': 'FUNCTION_RW',
    'if': 'IF_RW',
    'return': 'RETURN_KW',
    'elif': 'ELIF_RW',
    'and': 'AND_RW',
    'else': 'ELSE_RW',
    'while': 'WHILE_RW',
    'exit': 'EXIT_RW',
    'for': 'FOR_RW',
    'not': 'NOT_RW',
    'in': 'IN_RW',
    'or': 'OR_RW',
    'skip': 'SKIP_RW',
    'display': 'DISPLAY_RW',
    'get': 'GET_RW',
    'constant': 'CONSTANT_RW',
    'plot_sint': 'PLOT_SINT_RW',
    'plot_cint': 'PLOT_CINT_RW',
    'plot_sc': 'PLOT_SC_RW',
    'plot_loan': 'PLOT_LOAN_RW',
    'plot_yr': 'PLOT_YR_RW',
    'plot_coup': 'PLOT_COUP_RW',
    'simple_interest': 'SINT_RW',
    'compound_interest': 'CINT_RW',
    'simple_annuity': 'SANN_RW',
    'stock_dividend': 'STOCKDIV_RW',
    'div_pershare': 'DPS_RW',
    'yield_ratio': 'YRATIO_RW',
    'coupon_payment': 'COUP_PAYMENT_RW',
    'coupon_amount': 'COUP_AMOUNT_RW',
    'loanfv_pin': 'LFV_PIN_RW',
    'loanfv_rtm': 'LFV_RTM_RW',
    'loan_principal': 'LPRINCIPAL_RW',
    'range': 'RANGE_RW'
}

INVALID = 'INVALID_TOKEN'


class Token:
    def __init__(self, type, lexeme, lineno, index, end, error):
        self.type = type                # represents the token
        self.lexeme = lexeme            # lexeme found in the code
        self.lineno = lineno            # represents the line number
        self.index = index              # starting index of the lexeme
        self.end = end                  # position of the last character of lexeme
        self.error = error              # any error message associated with the token

    def __repr__(self):
        if self.error:
            return f"Token(type='{self.type}', lexeme='{self.lexeme}', lineno={self.lineno}, index={self.index}, end={self.end}, error={self.error})"
        else:
            return f"Token(type='{self.type}', lexeme='{self.lexeme}', lineno={self.lineno}, index={self.index}, end={self.end})"


class Lexer:
    
    def __init__(self, code):
        self.code = code                # stores the input file
        
    # Returns the list of code by line
    def pass_data(self):
        lines = self.code.split('\n') 
        return lines
    
    def tokenize(self):
        IDENTIFIER = r'(_*[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)*)+'
        INT = r'[1-9]\d*'
        FLOAT = r'[1-9]\d*\.\d+'
        STRING = r'(\"([^"\n]*)\")|(\'([^"\n]*)\')'
        
        # Compile the list of tokens and their associated info
        tokens = []
        lineno = 0
        end = 0
        in_multiline_comment = False
        
        lines = self.code.split('\n')

        for lineno, line in enumerate(lines, start=1):
            index = 0           # Reset index for the next line

            while index < len(line):
                char = line[index]      # checks the code by line and by character
                lexeme = char           # stores the identified lexeme in the token
                start = index           # stores the starting index of a lexeme
                error = ''
                
                
                # Ignore whitespace
                if char in ' \t':
                    index += 1
                    continue  
                
                
                # Handles alphabetic characters and underscores
                if char.isalpha() or char == '_':
                    
                    # Inside multiline comment
                    if in_multiline_comment:
                        if line.endswith('##'):
                            lexeme = line[index:-2]
                            token_type = 'MULT_COM'
                            index += len(line)         
                            tokens.append(Token(token_type, lexeme, lineno, start, end, error))
                            lexeme = line[-2:]
                            token_type = 'MULT_COM_END'
                            index += len(line)
                            in_multiline_comment = False
                        else:
                            lexeme = line[index:]
                            token_type = 'MULT_COM'
                            index += len(line)     
                    else:
                        # Identifier, keyword, or reserved word
                        while index + 1 < len(line) and (line[index + 1].isalnum() or line[index + 1] == '_'):
                            index += 1
                            lexeme += line[index]

                        if lexeme in reserved_words:
                            token_type = reserved_words[lexeme]
                        elif lexeme in keywords:
                            token_type = keywords[lexeme]
                        else:
                            if re.search(IDENTIFIER, lexeme):
                                token_type = 'ID' 
                            else:
                                token_type = INVALID
                                error = 'Invalid syntax for identifier'
                                
                                
                # Handles numeric characters (integers or floats)                
                elif char.isdigit():
                    # Integer or float
                    while index + 1 < len(line) and (line[index + 1].isdigit() or line[index + 1] == '.'):
                        index += 1
                        lexeme += line[index]

                    if '.' in lexeme:
                        if re.match(FLOAT, lexeme):
                            token_type = 'FLOAT'
                        else:  
                            token_type = INVALID
                            error = "Invalid float literal"
                    else:
                        token_type = 'INT'
                        
                        
                # Handles string literals
                elif char in ['"', "'"]:
                    # String
                    quote_char = char
                    index += 1
                    while index < len(line) and line[index] != quote_char:
                        lexeme += line[index]
                        index += 1
                    if index < len(line):
                        lexeme += line[index]  # Include the closing quote
                        index += 1
                    if re.match(STRING, lexeme):
                        token_type = 'STRING' 
                    else:
                        token_type = INVALID
                        error = 'Unterminated string literal'
                 
                 
                # Handles operators     
                elif char in operator_deli:
                    # Check for longer operators first
                    found_operator = False
                    for op in sorted(operator_deli.keys(), key=len, reverse=True):
                        if line[index:].startswith(op):
                            lexeme = op
                            index += len(op) - 1
                            found_operator = True
                            token_type = operator_deli[lexeme]
                            break
                        else:
                            # No longer operator_deli found, use the single-character operator_deli
                            token_type = operator_deli[char]
                    if not found_operator:
                        token_type = INVALID
                        error = 'Invalid Syntax'
                 
                 
                # Handles multiline comments (## ... ##)       
                elif line[index:].startswith('##') and not in_multiline_comment:
                        in_multiline_comment = True
                        lexeme = '##'
                        token_type = 'MULT_COM_START'
                        index = len(line)
                        tokens.append(Token(token_type, lexeme, lineno, start, end, error))
                        if line[-2:].endswith('##'):
                            lexeme = '##'
                            token_type = 'MULT_COM_END'
                            index = len(line)
                            in_multiline_comment = False
                            continue
                        else: 
                            continue                                        
                elif in_multiline_comment and line[index:].startswith('##'):
                    # End of multiline comment
                    lexeme = '##'
                    token_type = 'MULT_COM_END'
                    in_multiline_comment = False
                    index += 2
                 
                
                # Handles single-line comments (#)       
                elif char == '#':
                    # Single-line comment
                    lexeme = line[index:]
                    token_type = 'SINGLE_COM'
                    index = len(line)


                # Handle other characters as invalid tokens
                else:
                    token_type = INVALID
                    lexeme = char
                    error = f"Unexpected token '{lexeme}'"
                    
                if token_type == INVALID and not error:
                    error = 'Invalid Syntax'
                    
                # Stores the tokens in the list    
                end = index
                tokens.append(Token(token_type, lexeme, lineno, start, end, error))
                index += 1          # increment to check the next character

        print(tokens)
        return tokens



def run(tokens):
    # sets the name of the file generated for the symbol table
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    output_file_path = f"Symbol Table_{timestamp}.cash"
    
    
    # style of the symbol table
    table = PrettyTable(['Line Number', 'Lexeme', 'Token', 'Index', 'Error'])
    table.title = "S Y M B O L   T A B L E"
    table._max_width = {"Lexeme" : 20, "Error": 20}
    table._min_width = {"Token": 20, "Index": 10}
    table.set_style(ORGMODE)

    for token in tokens:
        table.add_row([token.lineno, token.lexeme, token.type, token.index+1, token.error], divider=True)
    
    
    # If you don't want to generate a file for the symbol table, you can comment out the following lines or the return code.
    # This will prevent the creation of a file and only display the symbol table as output in the console.
    with open(output_file_path, 'w') as output_file:
        output_file.write(table.get_string())
    
    
    print(table)
    return f"{table}"


# Example usage
input_text = """
x = 5
y = 5
display(y)
z = x * y
display(z)
x+++
if y > 5:
    display("y is not greater than 5")
else:
    display("y is greater than 5)

for x in range(0, 3):
    display(x)

while x < 8:
    display(x)
    x++
compound_interest(10000, 2, 1)

y = 11
display(y < 5 | y < 10)
# plot_cint([1000, 5, 10, 2], [1500, 3, 8, 4])

"""
lexer = Lexer(input_text)
tokens = lexer.tokenize()
run(tokens)


