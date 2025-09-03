import re
from collections import defaultdict

# Function to eliminate immediate left recursion
def eliminate_left_recursion(non_terminal, productions):
    alpha = []  # recursive parts
    beta = []   # non-recursive parts
    
    for prod in productions:
        if prod.startswith(non_terminal):  # left recursive
            alpha.append(prod[len(non_terminal):])
        else:
            beta.append(prod)

    if not alpha:
        return {non_terminal: productions}  # no recursion

    new_non_terminal = non_terminal + "'"
    result = {
        non_terminal: [b + new_non_terminal for b in beta],
        new_non_terminal: [a + new_non_terminal for a in alpha] + ['ε']
    }
    return result


# Function to left-factor productions
def left_factoring(non_terminal, productions):
    prefix_dict = defaultdict(list)
    for prod in productions:
        prefix_dict[prod[0]].append(prod)

    if all(len(v) == 1 for v in prefix_dict.values()):
        return {non_terminal: productions}  # no factoring needed

    new_non_terminal = non_terminal + "'"
    factored = []
    new_prods = []

    for key, group in prefix_dict.items():
        if len(group) > 1:
            # common prefix factoring
            prefix = os.path.commonprefix(group)
            factored.append(prefix + new_non_terminal)
            suffixes = [g[len(prefix):] or 'ε' for g in group]
            new_prods.extend(suffixes)
        else:
            factored.append(group[0])

    return {
        non_terminal: factored,
        new_non_terminal: new_prods
    }


# Main
if __name__ == "__main__":
    import os

    grammar = {
        "E": ["E+T", "T"],
        "T": ["T*F", "F"],
        "F": ["(E)", "id"]
    }

    print("Original Grammar:")
    for nt, prods in grammar.items():
        print(f"{nt} -> {' | '.join(prods)}")

    new_grammar = {}
    # Step 1: Eliminate left recursion
    for nt, prods in grammar.items():
        result = eliminate_left_recursion(nt, prods)
        new_grammar.update(result)

    print("\nAfter Eliminating Left Recursion:")
    for nt, prods in new_grammar.items():
        print(f"{nt} -> {' | '.join(prods)}")

    # Step 2: Left Factoring
    factored_grammar = {}
    for nt, prods in new_grammar.items():
        result = left_factoring(nt, prods)
        factored_grammar.update(result)

    print("\nAfter Left Factoring:")
    for nt, prods in factored_grammar.items():
        print(f"{nt} -> {' | '.join(prods)}")

