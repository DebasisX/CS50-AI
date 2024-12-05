import sys
from crossword import *
import copy


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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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

        # suppose x is a variable and I traverse the domains of self and remove values that are out of order.

        temp = copy.deepcopy(self.domains)
        for key, values in temp.items():
            for value in values:
                if len(value) != key.length:
                    self.domains[key].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # objective: to make the var x and and y to be consistent to each other.
        # too make the following changes

        # Since x to y are to be made arc consistent.
        # x.domains.overlap is the index for the overlap e.g.: (0, 1)
        changes = False
        temp = []
        ls = list(self.crossword.overlaps[x, y])
        if ls == []:
            return False
        for wordx in self.domains[x]:
            flag = False
            for wordy in self.domains[y]:
                if wordx[ls[0]] == wordy[ls[1]]:
                    flag = True
                    break
            if flag == False:
                temp.append(wordx)
                changes = True
        for i in temp:
            self.domains[x].remove(i)
        if changes == True:
            return True
        return False
        # Done

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # ok, arc is a tuple (x, y)
        if arcs is None:
            queue = [(x, y) for x in self.domains for y in self.crossword.neighbors(x)]
        else:
            queue = list(arcs)

        while len(queue) > 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for i in self.domains:
            if i not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        used = set()

        for var, word in assignment.items():
            # word fits?
            if len(word) != var.length:
                return False

            # uniqueness
            if word in used:
                return False
            used.add(word)

            # conflicts with neighboring slots check
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps.get((var, neighbor))
                    if overlap:
                        i, j = overlap
                        # characters match
                        if word[i] != assignment[neighbor][j]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # count the least values that are removed
        neighbours = self.crossword.neighbors(var)
        temp = {}
        for i in self.domains[var]:
            count = 0
            for neighbour in neighbours:
                if i in self.domains[neighbour]:
                    count += 1
            temp[i] = count

        temp = sorted(temp, key=temp.get)
        return temp

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        minimum = float('inf')

        for i in self.domains:
            if i not in assignment:

                if len(self.domains[i]) < minimum:
                    minimum = len(self.domains[i])
                    selected = i

                elif len(self.domains[i]) == minimum:
                    neighbors = len(self.crossword.neighbors(i))
                    selected = len(self.crossword.neighbors(selected))

                    if neighbors < selected:
                        selected = i

        return selected

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # tap in the backtrack code from the slide
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        val = self.order_domain_values(var, assignment)
        for i in val:
            assignment[var] = i
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)
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
