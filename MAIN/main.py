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


def parse_factor(tokens):
    token = tokens.pop(0)
    return int(token)


def parse_term(tokens):
    value = parse_factor(tokens)
    
    while tokens and tokens[0] in ("*", "/"):
        op = tokens.pop(0)
        right = parse_factor(tokens)

        if op == "*":
            value *= right

        else:
            value /= right
    
    return value


def parse_expression(tokens):
    value = parse_term(tokens)
    
    while tokens and tokens[0] in ("+", "-"):
        op = tokens.pop(0)
        right = parse_term(tokens)
    
        if op == "+":
            value += right

        else:
            value -= right
    
    return value


def evaluate(tokens):
    tokens = tokens[:]
    result = parse_expression(tokens)
    
    if isinstance(result, float) and result.is_integer():
        return int(result)
    
    return result
    

while True:
    try:
        line = input(">>> ")
        tokens = tokenize(line)
        result = evaluate(tokens)
        print(result)
    
    except Exception as e:
        print("Error:", e)