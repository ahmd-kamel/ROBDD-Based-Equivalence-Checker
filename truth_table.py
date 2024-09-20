import itertools
from boolean_parser import *

def evaluate_parsed_expression(parsed_expr, var_values):
    for var, value in var_values.items():
        # \b{var}\b ensures that var bounded by non-character.
        parsed_expr = re.sub(rf'\b{var}\b', str(value), parsed_expr)
    return eval(parsed_expr)
    

def generate_truth_table(expression):
    truth_table = []
    variables = extract_variables(expression)
    parsed_expr = parse_boolean_expression(expression)
    truth_values = list(itertools.product([False, True], repeat=len(variables)))

    print(f"{' '.join(variables)} | Result")
    print("-" * (len(variables) * 2 + 8))

    for values in truth_values:
        var_values = dict(zip(variables, values))
        result = evaluate_parsed_expression(parsed_expr, var_values)
        truth_table.append((values, result))
        print(f"{' '.join([str(int(v)) for v in values])} | {int(result)}")
        
    print("\n")
    return truth_table


def compare_truth_tables(table1, table2):
    if len(table1) != len(table2):
        return False

    for row1, row2 in zip(table1, table2):
        # compare the result (true/false) columns
        if row1[1] != row2[1]:
            return False
    return True