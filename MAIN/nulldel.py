def reset_variable(var_name, variables, constants):
    if not var_name.isalpha():
        raise ValueError("Invalid variable name")
    
    if var_name in constants:
        raise ValueError(f"'{var_name}' is a constant and cannot be changed")
    
    if var_name in variables:
        variables[var_name] = None
        print(f"'{var_name}' reset to null")
    
    else:
        variables[var_name] = None
        print(f"'{var_name}' set to null")

def delete_variable(var_name, variables, constants):
    if not var_name.isalpha():
        raise ValueError("Invalid variable name")
    
    if var_name in constants:
        raise ValueError(f"'{var_name}' is a constant and cannot be changed")
    
    if var_name in variables:
        del variables[var_name]
        print(f"'{var_name}' deleted")
    
    else:
        print(f"'{var_name}' does not exist")
