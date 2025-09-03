# LL(1) Parser Implementation in Python

# Parsing table for grammar
# E  -> T E'
# E' -> + T E' | ε
# T  -> F T'
# T' -> * F T' | ε
# F  -> ( E ) | id

parsing_table = {
    ('E', 'id'): ['T', "E'"],
    ('E', '('): ['T', "E'"],
    ("E'", '+'): ['+', 'T', "E'"],
    ("E'", ')'): ['ε'],
    ("E'", '$'): ['ε'],
    ('T', 'id'): ['F', "T'"],
    ('T', '('): ['F', "T'"],
    ("T'", '*'): ['*', 'F', "T'"],
    ("T'", '+'): ['ε'],
    ("T'", ')'): ['ε'],
    ("T'", '$'): ['ε'],
    ('F', 'id'): ['id'],
    ('F', '('): ['(', 'E', ')']
}


def ll1_parse(tokens):
    stack = ['$','E']   # bottom marker + start symbol
    i = 0
    a = tokens[i]

    print(f"{'Stack':<20}{'Input':<20}{'Action'}")
    print("-"*50)

    while len(stack) > 0:
        top = stack[-1]

        # Print step
        print(f"{''.join(stack):<20}{''.join(tokens[i:]):<20}", end='')

        # If both are terminals
        if top == a:
            print(f"Match {a}")
            stack.pop()
            i += 1
            a = tokens[i]
        elif top == 'ε':
            stack.pop()
            print("ε-production")
        elif (top, a) in parsing_table:
            stack.pop()
            production = parsing_table[(top, a)]
            if production != ['ε']:
                stack.extend(reversed(production))
            print(f"{top} -> {' '.join(production)}")
        else:
            print("Error: no rule")
            return False

        if top == '$' and a == '$':
            break

    return True


# Test
if __name__ == "__main__":
    # Example input string: id + id * id
    input_tokens = ['id', '+', 'id', '*', 'id', '$']

    accepted = ll1_parse(input_tokens)
    if accepted:
        print("\nString Accepted!")
    else:
        print("\nString Rejected!")
