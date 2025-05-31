from main import *
from nulldel import *
from linehandler import handle_line

script_path = input("Enter the script filename: ").strip()

try:
    with open(script_path, "r") as file:
        lines_iter = iter(file)
        
        for line in lines_iter:
            line = line.strip()
            
            if line:
                try:
                    handle_line(line, lines_iter)
                
                except Exception as e:
                    print(f"Error on line '{line}':", e)

except FileNotFoundError:
    print(f"File '{script_path}' not found.")