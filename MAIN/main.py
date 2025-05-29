# Converts input to tokens
def tokenize(expr):
    tokens = []
    number = ''
    
    for char in expr:
        if char.isdigit():
            number += char
    
        elif char in "+-*/()^!":
            if number:
                tokens.append(number)
                number = ''

            if char == "!" and tokens and tokens[-1] == "!":
                tokens[-1] = "!!"
            
            else:
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
    if not tokens:
        raise ValueError("Unexpected end of input")
    
    token = tokens.pop(0)

    if token == "(":
        value = parse_expression(tokens)

        if not tokens or tokens.pop(0) != ")":
            raise ValueError("Expected ')'")
    
    else:
        value = int(token)

    while tokens and tokens[0] in ("!", "!!"):
        op = tokens.pop(0)
        
        if not isinstance(value, int) or value < 0:
            raise ValueError("Factorial only works on non-negative integers")
        
        if op == "!":
            value = factorial(value)
        
        elif op == "!!":
            value = double_facorial(value)

    return value


def parse_term(tokens):
    value = parse_power(tokens)
    
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


def parse_power(tokens):
    value = parse_factor(tokens)

    while tokens and tokens[0] == "^":
        tokens.pop(0)
        right = parse_power(tokens)
        value = value ** right

    return value


def factorial(n):
    if n == 0 or n == 1:
        return 1
    
    result = 1
    
    for i in range(2, n + 1):
        result *= i
    
    return result


def double_facorial(n):
    if n < 0:
        raise ValueError("Double factorial not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    
    for i in range(n, 0, -2):
        result *= i

    return result


def evaluate(tokens):
    tokens = tokens[:]
    result = parse_expression(tokens)
    
    if isinstance(result, float) and result.is_integer():
        return int(result)
    
    return result
    

# CLI screen and input handler
while True:
    try:
        line = input(">>> ")
        tokens = tokenize(line)
        result = evaluate(tokens)
        print(result)
    
    except Exception as e:
        print("Error:", e)