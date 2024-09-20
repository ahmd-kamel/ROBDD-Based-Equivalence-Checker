import re

"""
- Define all the logical operators XOR, AND, OR, NOT, NOR and NAND.
  Any boolean expression can be mapped using those functions
"""
def XOR(a, b):
    return a ^ b

def AND(a, b):
    return a & b

def OR(a, b):
    return a | b

def NOT(a):
    return not a

def NOR(a, b):
    return not (a | b)

def NAND(a, b):
    return not (a & b)

def extract_variables(expr):
    return sorted(set(re.findall(r'[A-Za-z][A-Za-z0-9]*', expr)))



def parse_boolean_expression(expr):
    tokens = re.findall(r'[A-Za-z][A-Za-z0-9]*|[\^&|~!()]', expr)

    def evaluate_expression(tokens):
        def parse_factor():
            token = tokens.pop(0)
            if token == '(':
                result = parse_expression()
                tokens.pop(0)
                return result
            elif token == '~' or token == '!':
                return f'NOT({parse_factor()})'
            return token

        def parse_term():
            result = parse_factor()
            while tokens and tokens[0] == '^':
                tokens.pop(0)
                result = f'XOR({result}, {parse_factor()})'
            return result

        def parse_expression():
            result = parse_term()
            while tokens and tokens[0] in '&|':
                op = tokens.pop(0)
                if op == '&':
                    if tokens and tokens[0] == '~':
                        tokens.pop(0)
                        result = f'NAND({result}, {parse_term()})'
                    else:
                        result = f'AND({result}, {parse_term()})'
                elif op == '|':
                    if tokens and tokens[0] == '~':
                        tokens.pop(0)
                        result = f'NOR({result}, {parse_term()})'
                    else:
                        result = f'OR({result}, {parse_term()})'
            return result
        
        return parse_expression()
    
    return evaluate_expression(tokens)