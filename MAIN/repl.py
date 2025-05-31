from main import *

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
