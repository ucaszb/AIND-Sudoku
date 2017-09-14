assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for box1 in unit:
            for box2 in unit:
                if box1 != box2 and values[box1] == values[box2] and len(values[box1]) == 2:
                    digit = values[box1]
                    for box in unit:
                        if box != box1 and box != box2:
                            for d in digit:
                                if d in values[box]:
                                    value = values[box].replace(d, '')
                                    values = assign_value(values, box, value)
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
boxes  = cross(rows, cols)
row_unit = [cross(r, cols) for r in rows]
col_unit = [cross(rows, c) for c in cols]
square_unit = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_unit = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
#diagonal_unit = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_unit + col_unit + square_unit + diagonal_unit
units = dict((box, [unit for unit in unitlist if box in unit]) for box in boxes)
peers = dict((box, set(sum(units[box],[])) - set([box])) for box in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = dict(zip(boxes, grid))
    for box in boxes:
        if values[box] not in digits:
            values = assign_value(values, box, digits)
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print (''.join(values[r + c].center(width) + ('|' if c in '36' else '')for c in cols))
        if r in 'CF':
            print (line)
    return

def eliminate(values):
    solved_values = [box for box in boxes if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            value = values[peer].replace(digit, '')
            values = assign_value(values, peer, value)
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplace = [box for box in unit if digit in values[box]]
            if len(dplace) == 1:
                values = assign_value(values, dplace[0], digit)
    return values

def reduce_puzzle(values):
    """
    Find the solution using eliminate, only_choice and naked_twins methods.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        the final status of values these methods can solve. If the sudoku doesn't have a solution, return False.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in boxes if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in boxes if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in boxes if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values
    nums, box_min = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    for digit in values[box_min]:
        new_values = values.copy()
        new_values[box_min] = digit
        attempt = search(new_values)
        if attempt:
            return attempt
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
