from main import *
from nulldel import *
from linehandler import handle_lines

script_path = input("Enter the script filename: ").strip()

try:
    with open(script_path, "r") as file:
        lines = [line.rstrip() for line in file if line.strip()]
        handle_lines(iter(lines))

except FileNotFoundError:
    print(f"File '{script_path}' not found.")
