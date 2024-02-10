import re
import traceback
from finalparser import *
from new_function import *
from plot import *
from lexer import Token, Lexer


file = r'sample.cash'
f = open(file,  'r')
data = f.read()   

table_values = Tables_Values()
parser = Parser(table_values)
lexer = Lexer(data)
try:
    tokens = lexer.pass_data()
    res = parser.parse_code(tokens)
    result = table_values.get_terminal() 
except:
    traceback.print_exc()
