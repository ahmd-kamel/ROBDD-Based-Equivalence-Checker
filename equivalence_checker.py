import sys
from graphviz import Source
from boolean_parser import *
from robdd_graph import *
from truth_table import *


if len(sys.argv) == 3:
    print("\n------------ Equivalence Checker Report ------------\n")
    fun_expression_1 = sys.argv[1]
    print("First Function:", parse_boolean_expression(fun_expression_1))
    table_1 = generate_truth_table(fun_expression_1)
    fun_robdd_1 = generate_robdd(fun_expression_1)

    fun_expression_2 = sys.argv[2]
    print("Second Function:", parse_boolean_expression(fun_expression_2))
    table_2 = generate_truth_table(fun_expression_2)
    fun_robdd_2 = generate_robdd(fun_expression_2)

    fun_robdd_dot_1 = robdd_to_dot(fun_robdd_1)
    fun_robdd_dot_2 = robdd_to_dot(fun_robdd_2)

    src_1 = Source(fun_robdd_dot_1)
    src_2 = Source(fun_robdd_dot_2)

    src_1.render("fun_robdd_1", format='png', cleanup=True)
    src_2.render("fun_robdd_2", format='png', cleanup=True)

    equivalent = compare_bdds_with_variable_mapping(fun_robdd_1, fun_robdd_2)

    if equivalent:
        print("- The ROBDDs are equivalent.\n")
    else:
        print("- The ROBDDs are not equivalent.\n")

    # Compare the truth tables
    if compare_truth_tables(table_1, table_2):
        print("- The expressions are equivalent formally.\n")
    else:
        print("- The expressions are not equivalent formally.\n")
else:
    print("Invalid number of arguments.")
