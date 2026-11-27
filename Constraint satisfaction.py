# Practical 6 — Constraint satisfaction: map colouring and 8-Queens
# Run: python P6_csp.py
# Library: none. Only plain Python 3


# ==========================================
# PART 1: MAP COLOURING (Australia Map)
# ==========================================


def is_safe_color(region, color, assignment, neighbors):
    """Check if assigning 'color' to 'region' violates any neighbor constraints."""
    for neighbor in neighbors[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True


def solve_map_coloring(regions, colors, neighbors, assignment={}):
    """Backtracking solver for the Map Colouring problem."""
    # Base case: all regions are colored
    if len(assignment) == len(regions):
        return assignment

    # Select the next unassigned region
    unassigned = [r for r in regions if r not in assignment]
    current_region = unassigned[0]

    # Try each available color
    for color in colors:
        if is_safe_color(current_region, color, assignment, neighbors):
            assignment[current_region] = color

            # Recursively assign colors to remaining regions
            result = solve_map_coloring(regions, colors, neighbors, assignment)
            if result is not None:
                return result

            # Backtrack if no valid solution was found down this path
            del assignment[current_region]

    return None


# ==========================================
# PART 2: 8-QUEENS PROBLEM
# ==========================================


def is_safe_queen(board, row, col, n):
    """Check if placing a queen at (row, col) is safe from attacks."""
    # Check column above
    for i in range(row):
        if board[i] == col:
            return False

    # Check upper-left diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if board[i] == j:
            return False

    # Check upper-right diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
        if board[i] == j:
            return False

    return True


def solve_n_queens(n=8, row=0, board=None):
    """Backtracking solver for the N-Queens problem.

    'board' is a 1D list where index = row and value = column of the queen.
    """
    if board is None:
        board = [-1] * n

    # Base case: all N queens are placed
    if row == n:
        return board

    # Try placing a queen in each column of the current row
    for col in range(n):
        if is_safe_queen(board, row, col, n):
            board[row] = col

            # Recurse for the next row
            result = solve_n_queens(n, row + 1, board)
            if result is not None:
                return result

            # Backtrack
            board[row] = -1

    return None


def print_chessboard(board):
    """Helper function to visually print the 8x8 board."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    print("=" * 45)
    print("1. MAP COLOURING CSP (Australia)")
    print("=" * 45)

    regions = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    colors = ["Red", "Green", "Blue"]
    neighbors = {
        "WA": ["NT", "SA"],
        "NT": ["WA", "SA", "Q"],
        "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"],
        "NSW": ["Q", "SA", "V"],
        "V": ["SA", "NSW"],
        "T": [],
    }

    map_solution = solve_map_coloring(regions, colors, neighbors)

    if map_solution:
        print("Solution found:")
        for region, color in map_solution.items():
            print(f"  {region:<4} -> {color}")
    else:
        print("No solution exists.")

    print("\n" + "=" * 45)
    print("2. 8-QUEENS CSP")
    print("=" * 45)

    queens_solution = solve_n_queens(8)

    if queens_solution:
        print("Queen column positions per row (0-indexed):", queens_solution)
        print("\nBoard Layout:")
        print_chessboard(queens_solution)
    else:
        print("No solution exists.")
