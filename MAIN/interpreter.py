from main import *
from nulldel import *
from linehandler import handle_lines
from collections import deque

script_path = input("Enter the script filename: ").strip()

try:
    with open(script_path, "r") as file:
        lines = deque(line.rstrip() for line in file if line.strip())
        handle_lines(lines)

except FileNotFoundError:
    print(f"File '{script_path}' not found.")