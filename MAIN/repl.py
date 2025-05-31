from main import *
from linehandler import *
from nulldel import *

while True:
    try:
        line = input(">>> ").strip()
        line_iter = iter(line)
        handle_line(line, line_iter)
    
    except Exception as e:
        print("Error:", e)
