def tokenize(expr):
    tokens = []
    number = ''
    for char in expr:
        if char.isdigit():
            number += char
        elif char in "+-*/":
            if number:
                tokens.append(number)
                number = ''
            tokens.append(char)
        elif char.isspace():
            if number:
                tokens.append(number)
                number = ''
        else:
            raise ValueError(f"Invalid character: {char}")
    
    if number:
        tokens.append(number)
    
    return tokens

def evaluate(tokens):
    if len(tokens) != 3:
        raise ValueError("Only simple expressions like '1 + 2' are currntly supported.")
    
    left = int(tokens[0])
    op = tokens[1]
    right = int(tokens[2])

    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        return left / right
    else:
        raise ValueError(f"Unknown operator: {op}")
    
while True:
    try:
        line = input(">>> ")
        tokens = tokenize(line)
        result = evaluate(tokens)
        print(result)
    except Exception as e:
        print("Error:", e)