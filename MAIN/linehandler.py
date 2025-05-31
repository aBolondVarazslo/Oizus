from main import *
from nulldel import *

def handle_line(line, lines_iter):
    if line.startswith("#"):
        return
    
    if not line:
        return

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

    elif line.startswith("null "):
        var_name = line[len("null "):].strip()
        reset_variable(var_name, variables, constants)

    elif line.startswith("del "):
        var_name = line[len("del "):].strip()
        delete_variable(var_name, variables, constants)

    elif line.startswith("if ") and line.endswith(":"):
        condition_expr = line[3:-1].strip()
        condition_tokens = tokenize(condition_expr)
        condition_result = evaluate(condition_tokens)

        block_lines = read_block(lines_iter)

        if condition_result:
            for blk_line in block_lines:
                handle_line(blk_line, lines_iter)

    else:
        equal_pos = line.find('=')

        if equal_pos != -1 and not (
            (equal_pos + 1 < len(line) and line[equal_pos + 1] == '=') or
            (equal_pos > 0 and line[equal_pos - 1] in ('!', '<', '>'))
        ):
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
            tokens = tokenize(line)
            result = evaluate(tokens)
            print(result)


def read_block(lines_iter):
    block_lines = []

    for line in lines_iter:
        line = line.strip()
        if line == "done":
            break
        block_lines.append(line)
    
    return block_lines