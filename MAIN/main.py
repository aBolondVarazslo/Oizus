# Converts input to tokens
def tokenize(expr):
    tokens = []
    number = ''
    identifier = ''
    in_string = False
    string_delim = ''
    string_buffer = ''
    i = 0

    while i < len(expr):
        char = expr[i]

        if in_string:
            if char == '\\':  # Escape character
                i += 1
                if i < len(expr):
                    string_buffer += expr[i]
                else:
                    raise ValueError("Unfinished escape sequence in string")

            elif char == string_delim:
                tokens.append(string_delim + string_buffer + string_delim)
                string_buffer = ''
                in_string = False

            else:
                string_buffer += char

        else:
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

            elif char in "+-*/()^!<>=:":
                if number:
                    tokens.append(number)
                    number = ''
                if identifier:
                    tokens.append(identifier)
                    identifier = ''

                # Handle multi-character comparison operators
                if char in ('=', '!', '<', '>') and i + 1 < len(expr):
                    next_char = expr[i + 1]
                    two_char = char + next_char

                    if two_char in ('==', '!=', '<=', '>='):
                        tokens.append(two_char)
                        i += 1
                    elif char == '!':
                        # Handle multiple factorials
                        count = 1
                        while i + 1 < len(expr) and expr[i + 1] == '!':
                            count += 1
                            i += 1
                        tokens.append('!' * count)
                    else:
                        tokens.append(char)
                elif char == '!':
                    # Handle multiple factorials
                    count = 1
                    while i + 1 < len(expr) and expr[i + 1] == '!':
                        count += 1
                        i += 1
                    tokens.append('!' * count)
                else:
                    tokens.append(char)

            elif char in ('"', "'"):
                if number:
                    tokens.append(number)
                    number = ''
                if identifier:
                    tokens.append(identifier)
                    identifier = ''

                in_string = True
                string_delim = char
                string_buffer = ''

            elif char.isspace():
                if number:
                    tokens.append(number)
                    number = ''
                if identifier:
                    tokens.append(identifier)
                    identifier = ''

            else:
                raise ValueError(f"Invalid character: {char}")

        i += 1

    if in_string:
        raise ValueError("Unterminated string literal")

    if number:
        tokens.append(number)
    if identifier:
        tokens.append(identifier)

    return tokens


# Dictionaries
variables = {}
constants = {}
keywords = {"and", "or", "not", "if", "else", "while", "for"}


# Parses math
def parse_factor(tokens):
    if not tokens:
        raise ValueError("Unexpected end of input")
    
    token = tokens.pop(0)

    if token == "-":
        value = parse_factor(tokens)
        if isinstance(value, (int, float)):
            return -value
        
        else:
            raise ValueError("Unary negative can only be applied to numbers")


    if token == "(":
        value = parse_logical_or(tokens)

        if not tokens or tokens.pop(0) != ")":
            raise ValueError("Expected ')'")
    

    else:
        if token.isdigit():
            value = int(token)
        

        else:
            if token in variables:
                value = variables[token]

            elif token in constants:
                value = constants[token]
            
            elif isinstance(token, str) and (token.startswith('"') or token.startswith("'")):
                value = token[1:-1]
            
            else:
                raise ValueError(f"Undefined variable or invalid token: {token}")


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
            if isinstance(value, str) or isinstance(right, str):
                value = str(value) + str(right)
            
            else:
                value += right

        else:
            value -= right
    
    return value


def parse_comparison(tokens):
    value = parse_expression(tokens)

    while tokens and tokens[0] in ("==", "!=", ">", "<", ">=", "<="):
        op = tokens.pop(0)
        right = parse_expression(tokens)

        if op == "==":
            value = value == right
        
        elif op == "!=":
            value = value != right
        
        elif op == ">":
            value = value > right
        
        elif op == "<":
            value = value < right
        
        elif op == ">=":
            value = value >= right
        
        elif op == "<=":
            value = value <= right
        
    return value


def parse_power(tokens):
    value = parse_factor(tokens)

    while tokens and tokens[0] == "^":
        tokens.pop(0)
        right = parse_power(tokens)
        value = value ** right

    return value


# Parses logic
def parse_logical_not(tokens):
    if tokens and tokens[0] == "not":
        tokens.pop(0)
        value = parse_logical_not(tokens)
        return not value
    
    else:
        return parse_comparison(tokens)


def parse_logical_and(tokens):
    value = parse_logical_not(tokens)

    while tokens and tokens[0] == "and":
        tokens.pop(0)
        right = parse_logical_not(tokens)
        value = value and right

    return value


def parse_logical_or(tokens):
    value = parse_logical_and(tokens)

    while tokens and tokens[0] == "or":
        tokens.pop(0)
        right = parse_logical_and(tokens)
        value = value or right
    
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
    result = parse_logical_or(tokens)

    if tokens:
        raise ValueError(f"Unexpected input after expression: {' '.join(tokens)}")
    
    if isinstance(result, float) and result.is_integer():
        return int(result)
    
    return result
    

# CLI screen and input handler
while True:
    try:
        line = input(">>> ").strip()

        if not line:
            continue

        if line.startswith("const "):
            rest = line[len("const "):].strip()

            if "=" not in rest:
                raise ValueError("Expected '=' in constant definition")

            const_name, expr = rest.split("=", 1)
            const_name = const_name.strip()
            expr = expr.strip()

            if not const_name.isalpha():
                raise ValueError("Invalid constant name")
            
            if const_name in keywords:
                raise ValueError(f"'{const_name}' is a reserved keyword and cannot be used for variables or constants")

            tokens = tokenize(expr)
            value = evaluate(tokens)
            constants[const_name] = value
            print(f"{const_name} (constant) = {value}")

        else:
            equal_pos = line.find('=')

            # Check if '=' is present and is a single assignment (not part of ==, !=, <=, >=)
            if equal_pos != -1 and not (
                (equal_pos + 1 < len(line) and line[equal_pos + 1] == '=') or
                (equal_pos > 0 and line[equal_pos - 1] in ('!', '<', '>'))
            ):
                # This is an assignment
                var_name = line[:equal_pos].strip()
                expr = line[equal_pos + 1:].strip()

                if not var_name.isalpha():
                    raise ValueError("Invalid variable name")
                
                if var_name in keywords:
                    raise ValueError(f"'{var_name}' is a reserved keyword and cannot be used for variables or constants")
                
                if var_name in constants:
                    raise ValueError(f"'{var_name}' is a constant and cannot be changed")

                tokens = tokenize(expr)
                value = evaluate(tokens)
                variables[var_name] = value
                print(f"{var_name} = {value}")

            else:
                # Otherwise, treat as an expression (including comparisons)
                tokens = tokenize(line)
                result = evaluate(tokens)
                print(result)

    except Exception as e:
        print("Error:", e)
