# Converts input to tokens
def tokenize(expr):
    tokens = []
    number = ''
    identifier = ''
    
    for char in expr:
        if char.isdigit():
            if identifier:
                tokens.append(identifier)
                identifier = ''
            
            number += char
        
        elif char.isalpha():
            if number:
                tokens.append(number)
                number = ''
            
            identifier += char
    
        elif char in "+-*/()^!":
            if number:
                tokens.append(number)
                number = ''
            
            if identifier:
                tokens.append(identifier)
                identifier = ''

            if char == "!" and tokens:
                if tokens[-1] == "!!":
                    tokens[-1] = "!!!"
                
                elif tokens[-1] == "!":
                    tokens[-1] = "!!"
                
                else:
                    tokens.append("!")
            
            else:
                tokens.append(char)
    
        elif char.isspace():
            if number:
                tokens.append(number)
                number = ''
            
            if identifier:
                tokens.append(identifier)
                identifier = ''
    
        else:
            raise ValueError(f"Invalid character: {char}")
    
    if number:
        tokens.append(number)

    if identifier:
        tokens.append(identifier)
    
    return tokens


# Variables dictionary
variables = {}

# Parses
def parse_factor(tokens):
    if not tokens:
        raise ValueError("Unexpected end of input")
    
    token = tokens.pop(0)

    if token == "(":
        value = parse_expression(tokens)

        if not tokens or tokens.pop(0) != ")":
            raise ValueError("Expected ')'")
    
    else:
        if token.isdigit():
            value = int(token)
        
        else:
            if token in variables:
                value = variables[token]
            
            else:
                raise ValueError(f"Undefined variable: {token}")

    while tokens and tokens[0] in ("!", "!!", "!!!"):
        op = tokens.pop(0)
        
        if not isinstance(value, int) or value < 0:
            raise ValueError("Factorial only works on non-negative integers")
        
        if op == "!":
            value = factorial(value)
        
        elif op == "!!":
            value = double_facorial(value)

        elif op == "!!!":
            value = triple_factorial(value)

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


# Calculates factorials
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


def triple_factorial(n):
    if n < 0:
        raise ValueError("Triple factorial no defined for negative numbers")
    
    if n == 0 or n == 1 or n == 2:
        return 1
    
    result = 1

    for i in range(n, 0, -3):
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
        if "=" in line:
            var_name, expr = line.split("=", 1)
            var_name = var_name.strip()
            expr = expr.strip()

            if not var_name.isalpha():
                raise ValueError("Invalid variable name")
            
            
            tokens = tokenize(expr)
            value = evaluate(tokens)
            variables[var_name] = value
            print(f"{var_name} = {value}")
        
        else:
            tokens = tokenize(line)
            result = evaluate(tokens)
            print(result)
    
    except Exception as e:
        print("Error:", e)