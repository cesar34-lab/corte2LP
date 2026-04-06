def detect_ambiguity(trees):
    return len(trees) > 1


def detect_associativity(tree):
    """
    Detecta asociatividad para expresiones tipo id + id + id
    """

    # Caso: (E (E ...) + T) → izquierda
    if (
        len(tree.children) == 3
        and hasattr(tree.children[0], "children")
    ):
        left = tree.children[0]

        if len(left.children) == 3:
            return "Left"

    # Caso: (E T + (E ...)) → derecha
    if (
        len(tree.children) == 3
        and hasattr(tree.children[2], "children")
    ):
        right = tree.children[2]

        if len(right.children) == 3:
            return "Right"

    return "Unknown"


def detect_precedence(tree):
    """
    Detecta si * tiene mayor precedencia que +
    """

    def find_operator_depth(node, target, depth=0):
        if not hasattr(node, "children"):
            return None

        if len(node.children) == 3:
            if node.children[1] == target:
                return depth

        depths = []
        for child in node.children:
            if hasattr(child, "children"):
                d = find_operator_depth(child, target, depth + 1)
                if d is not None:
                    depths.append(d)

        return min(depths) if depths else None

    plus_depth = find_operator_depth(tree, "+")
    mult_depth = find_operator_depth(tree, "*")

    if plus_depth is None or mult_depth is None:
        return "Unknown"

    if mult_depth > plus_depth:
        return "* > +"
    elif plus_depth > mult_depth:
        return "+ > *"
    else:
        return "Same precedence"
