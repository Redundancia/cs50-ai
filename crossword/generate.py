import sys

from numpy import var

from crossword import *
from queue import Queue

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for key,value in self.domains.items():
            for word in value.copy():
                if len(word) != key.length:
                    self.domains[key].remove(word)
        # print("self.domains after unary node consistency applied:")
        # print(self.domains)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision_made = False
        # 2 value can only overlap in one position if, if you make that word can change direction you will just need a for loop to get all overlaps
        
        # first we get the overlapping position
        overlapping_positions = self.crossword.overlaps[(x, y)]
        # print(f"overlapping position: {overlapping_positions}")
        # Quit asap if they have no overlap
        if overlapping_positions == None:
            return revision_made
        
        # print(f"self.domains[x]: {self.domains[x]}")
        for x_value in self.domains[x].copy():
            # print(f"self.domains' key {x}: value: {x_value}")
            at_least_one_y_corresponds = False
            for y_value in self.domains[y]:
                # check if in the 2 words, the corresponding characters are the same
                if x_value[overlapping_positions[0]] == y_value[overlapping_positions[1]]:
                    # print(f"there was a corresponding value, keep {x_value} for {y_value}")
                    at_least_one_y_corresponds = True
                    break
            if at_least_one_y_corresponds == False:
                # print(f"there was no corresponding value, trying to delete {x}")
                self.domains[x].remove(x_value)
                revision_made = True
        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # print("self.crossword.overlaps:")
        # print(self.crossword.overlaps)
        queue = Queue(maxsize = 0)
        # if arcs are empty, we just fill it up with every overlap/arc we have
        if arcs == None:
            for key, value in self.crossword.overlaps.items():
                queue.put(key)

        while not queue.empty():
            variable = queue.get()
            # print(variable)
            if self.revise(variable[0],variable[1]):
                # check if we have zero items left in our domain, if so we have no solution
                if len(self.domains[variable[0]]) == 0:
                    return False
                # print(f"crossword neighbors: {self.crossword.neighbors(variable[0])}")
                for neighbor in self.crossword.neighbors(variable[0]):
                    # i put this if here maybe redundant or wrong, if i leave this if out i don't think it will matter, but using this might save some time? 
                    if neighbor != variable[1]:
                        queue.put((neighbor,variable[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in assignment:
            # print(f"variable: {variable}")
            if variable == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # print('assignment:')
        # print(assignment)
        # print()
        values = set()
        for key,value in assignment.items():
            # check if length is correct
            if key.length != len(value):
                return False
            # gather them in set, duplicate words are not allowed
            if value in values:
                return False
            values.add(value)
        # neighboring variables have the proper correspondence
        # iterate over overlaps
        for overlap_key, overlap_value in self.crossword.overlaps.items():
            # print (overlap_key)
            # print (overlap_value)
            # if one of their values is still unassigned, move on to next one, same with overlap value being None
            if overlap_value == None or overlap_key[0] not in assignment.keys() or overlap_key[1] not in assignment.keys():
                continue
            # check if correspondence character is the same
            # print(f"assignemnt's overlap_key-s value something 0 lol: {assignment[overlap_key[0]]}")
            # print(f"assignemnt's overlap_key-s value something 1 lol: {assignment[overlap_key[1]]}")
            if assignment[overlap_key[0]][overlap_value[0]] != assignment[overlap_key[1]][overlap_value[1]]:
                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        list_of_values = [value for value in self.domains[var]]
        return list_of_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return variable
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        solution_found = True
        for variable in self.crossword.variables:
            if variable not in assignment:
                solution_found = False
                break
        if solution_found:
            return assignment
        
        #if all([True if variable in assignment.keys() else False for variable in self.crossword.variables]):
        #    return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
