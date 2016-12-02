import rexpy.ast as ast

# RE Grammar in use:
# R -> S "|" R (UnionASTNode)
# R -> S
# S -> T | TS (ConcatASTNode)
# T -> F | F "*" (StarASTNode)
# F -> C | "(" R ")"
# C -> C1 | "\" C2
# C1 -> <any character except "(", ")", "|", "*"> (AtomASTNode)
# C2 -> <any character> (AtomASTNode)

# The nice thing about the grammar table approach is that building a compiler-compiler later will just involve
# generating the grammar table for a BNF grammar and then using analagous logic to what I have here. One
# challenge will be using symbols in the grammar table that don't collide with terminals in the grammar.

# The issue with the grammar table is that we'd have to encode 'logic' into the grammar table, which can get
# messy. Although this is probably possible, I'll start with the function method first.

# I'll start with doing a recursive descent parser with backtracking and try predictive parsing
# later. Backtracking introduces the problem of exponential group and non-guaranteed termination for certain
# languages, but I'm pretty sure (?) this isn't an issue for my RE grammar.

# The non-guaranteed termination comes into play when we have a loop in the grammar that doesn't involve
# readig any new substances (i.e. well formed parentheses).

# Let's start by creating a parser that doesn't build up the AST, but just accepts or rejects input

# The below actually doesn't work... I need to convert my grammar to LL(1) form or something... Back to the
# drawing board :/

def re_string_to_ast2(re_str):
    (_, is_valid) = R(re_str, 0)
    return is_valid

def R(s, i):
    (i2, is_valid) = R1(s, i)
    if is_valid:
        return (i2, is_valid)

    (i2, is_valid) = R2(s, i)
    return (i2, is_valid)

# R -> S "|" R (Union)
def R1(s, i):
    (i2, is_valid) = S(s, i)
    if not is_valid:
        print("1")
        return (i2, False)

    (i3, is_valid) = term(s, i2, "|")
    if not is_valid:
        print("2")
        return (i3, False)

    (i4, is_valid) = R(s, i3)
    print("3")
    return (i4, is_valid)

def R2(s, i):
    return S(s, i)

def S(s, i):
    (i2, is_valid) = S1(s, i)
    if is_valid:
        return (i2, is_valid)

    return S2(i2, is_valid)

def S1(s, i):
    print("4")
    return T(s, i)

def S2(s, i):
    (i2, is_valid) = T(s, i)
    if not is_valid:
        print("5")
        return (i2, False)

    print("6")
    return S(s, i2)

# Temporarily, let T be any character except | for testing overall structure
def T(s, i):
    if i < len(s) and s[i] is not "|":
        return (i + 1, True)
    else:
        return (i, False)

def term(s, i, c):
    if i < len(s) and s[i] is c:
        return (i + 1, True)
    else:
        return (i, False)

def re_string_to_ast(re_str):
    nodes_to_concat = []

    prev_char = None
    for char in re_str:
        if prev_char is None and char is "*":
            raise ValueError("Regex string %s has leading '*' character!" % re_str)

        elif prev_char is "*" and char is "*":
            raise ValueError("Regex string %s has consecutive '*' characters!" % re_str)

        elif prev_char is not "*" and char is "*":
            prev_node = nodes_to_concat.pop()
            nodes_to_concat.append(ast.StarASTNode(prev_node))

        else:
            nodes_to_concat.append(ast.AtomASTNode(char))

        prev_char = char

    return ast.ConcatASTNode(nodes_to_concat)
