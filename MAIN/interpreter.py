from main import *
from nulldel import *
from linehandler import handle_line

script_path = input("Enter the script filename: ").strip()

try:
    with open(script_path, "r") as file:
        lines = [line.rstrip() for line in file if line.strip()]
        lines_iter = iter(lines)

        for line in lines_iter:
            handle_line(line, lines_iter)

except FileNotFoundError:
    print(f"File '{script_path}' not found.")
