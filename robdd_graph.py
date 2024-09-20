import re
from boolean_parser import *

class BDDNode:
    def __init__(self, var=None, high=None, low=None, terminal=None):
        self.var = var            # The variable for this node
        self.high = high          # The high branch (when the variable is True)
        self.low = low            # The low branch (when the variable is False)
        self.terminal = terminal  # Terminal value (True or False)

    def __eq__(self, other):
        if not isinstance(other, BDDNode):
            return False
        return (self.var == other.var and 
                self.low == other.low and 
                self.high == other.high and 
                self.terminal == other.terminal)
    
    def __hash__(self):
        # Use a tuple of the node's key properties to compute the hash
        return hash((self.var, self.high, self.low, self.terminal))
    
    def __repr__(self):
        if self.terminal is not None:
            return f"Terminal({self.terminal})"
        return f"Node({self.var}, High={self.high}, Low={self.low})"


# Apply Shannon expansion to build the BDD
def shannon_expansion(expr, var):
    positive_expr = re.sub(rf'\b{var}\b', 'True', expr)
    negative_expr = re.sub(rf'\b{var}\b', 'False', expr)  
    return positive_expr, negative_expr


# Evaluate an expression (used for terminal cases)
def evaluate_expr(expr):
    try:
        return eval(expr)
    except Exception:
        return None


node_cache = {}
def reduction(node):
    """ Apply reduction rules and cache the node. """
    # Rule 1: Eliminate redundant nodes
    if node.low == node.high:
        return node.low
    
    # Rule 2: Merge equivalent subtrees (Memoization)
    node_key = (node.var, id(node.low), id(node.high))
    if node_key in node_cache:
        return node_cache[node_key]
    
    node_cache[node_key] = node
    return node


# Recursive function to construct BDD using Shannon expansion
def construct_robdd_from_expression(parsed_expr, variables):
    # Base case: if the expression simplifies to True/False
    simplified = evaluate_expr(parsed_expr)
    if simplified is not None:
        return BDDNode(terminal=simplified)

    # Apply Shannon expansion for the current variable
    var = variables[0]
    rest_vars = variables[1:]
    pos_expr, neg_expr = shannon_expansion(parsed_expr, var)
    # Recursively construct the high and low branches
    high_node = construct_robdd_from_expression(pos_expr, rest_vars)
    low_node =  construct_robdd_from_expression(neg_expr, rest_vars)

    return reduction(BDDNode(var=var, high=high_node, low=low_node))


# Main function to generate and print the ROBDD
def generate_robdd(expression):
    # Extract variables and parse the expression
    variables = extract_variables(expression)
    parsed_expr = parse_boolean_expression(expression)

    # Construct the BDD using Shannon expansion
    return construct_robdd_from_expression(parsed_expr, variables)


# Function to compare two ROBDDs while considering variable renaming
def compare_bdds_with_variable_mapping(bdd1, bdd2, var_map=None):
    if var_map is None:
        var_map = {}

    # If both are terminal nodes, compare their values
    if bdd1.terminal is not None and bdd2.terminal is not None:
        return bdd1.terminal == bdd2.terminal

    # If only one is terminal and the other is not, they are not equivalent
    if (bdd1.terminal is not None) or (bdd2.terminal is not None):
        return False

    # Check if the variables are already mapped
    if bdd1.var in var_map:
        if var_map[bdd1.var] != bdd2.var:
            return False  # Inconsistent mapping
    else:
        var_map[bdd1.var] = bdd2.var  # Map the variable in BDD1 to BDD2

    # Recursively compare the high and low branches
    high_eq = compare_bdds_with_variable_mapping(bdd1.high, bdd2.high, var_map)
    low_eq =  compare_bdds_with_variable_mapping(bdd1.low, bdd2.low, var_map)

    return high_eq and low_eq


# Function to generate the DOT representation of the ROBDD
def robdd_to_dot(robdd):
    dot = ['digraph ROBDD {']
    
    node_counter = [0]  # Use a list to keep node IDs mutable within recursive functions
    node_map = {}  # Map to hold node to ID mapping

    def get_node_id(node):
        """Returns a unique node ID for a given node."""
        if node in node_map:
            return node_map[node]
        node_id = f"node{node_counter[0]}"
        node_map[node] = node_id
        node_counter[0] += 1
        return node_id

    def process_node(node):
        """Recursively process each node and generate DOT format for it."""
        node_id = get_node_id(node)

        if node.terminal is not None:
            # Terminal node (True or False)
            label = f"1" if node.terminal else f"0"
            dot.append(f'{node_id} [label="{label}", shape=box];')
        else:
            # Decision node
            dot.append(f'{node_id} [label="{node.var}"];')

            # Process low (False) branch with a dashed line
            low_id = get_node_id(node.low)
            process_node(node.low)
            dot.append(f'{node_id} -> {low_id} [label="0", style=dashed];')

            # Process high (True) branch with a solid line
            high_id = get_node_id(node.high)
            process_node(node.high)
            dot.append(f'{node_id} -> {high_id} [label="1"];')

    process_node(robdd)
    dot.append('}')
    
    return '\n'.join(dot)


# Function to print the BDD
def print_bdd(node, indent=0):
    prefix = "  " * indent
    if node.terminal is not None:
        print(f"{prefix}Terminal({node.terminal})")
    else:
        print(f"{prefix}Node({node.var})")
        print(f"{prefix}  High:")
        print_bdd(node.high, indent + 2)
        print(f"{prefix}  Low:")
        print_bdd(node.low, indent + 2)
