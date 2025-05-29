def tokenize(expr):
    return expr.strip().split()

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