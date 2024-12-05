import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set() # set of the mines

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set() # set of mines that are found

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines
# each cell is a pair (i, j) where i is the row number (ranging from 0 to height - 1)
# and j is the column number (ranging from 0 to width - 1).

class Sentence(): # each sentence has a set of cells within it and a count of how many of those cells are mines.
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        temp = set()
        if len(self.cells) == self.count:
            if self.count != 0:
                return self.cells
        return temp
# Implemented

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        temp = set()
        if self.count == 0:
            return self.cells # As all are safe
        return temp
# Implemented

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

# Implemented

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

# Implemented

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        # cell is a set (i, j) so mines can be from [i - 1 to i + 1] and [j - 1 to j + 1].

        temp = Sentence(cells=set(), count=0)
        for x in range(cell[0] - 1, cell[0] + 2):
            for y in range(cell[1] - 1, cell[1] + 2):
                if (x, y) != cell and 0 <= x < self.height and 0 <= y < self.width and not (x, y) in temp.known_mines():
                    self.mines.add((x, y))
                    temp.cells.add((x, y))
        temp.count = count
        self.knowledge.append(temp)
        # 3 functionalities added from specification.
        # I have current location set(cell) and count(no. of mines nearby)
        # I have knowledge[set(cells which can be mines), count]
        # Sentence is a list of Sentence instances



        # If count == 0 we know that all cells are safe
        tempx = Sentence(cells=set(), count=0)
        for i in self.knowledge:
            for j in self.knowledge:
                if i.cells.issubset(j.cells) and not j.cells.difference(i.cells) in tempx.known_mines():
                    tempx.cells.update(j.cells.difference(i.cells))
                    tempx.count = j.count - i.count
        self.knowledge.append(temp)
        # I have to add the functionality of to find inferences
        # from the knowledge I already have.


        for sentence in self.knowledge:
            safes = sentence.known_safes()
            temp1 = safes.copy()

            for cell in temp1:
                self.mark_safe(cell)
            mines = sentence.known_mines()
            temp2 = mines.copy()
            for cell in temp2:
                self.mark_mine(cell)

        for sentence in self.knowledge:
            if sentence.count == 0:
                for i in sentence.cells:
                    self.mark_safe(i)
                    self.safes.add(i)




# Implement this. 5

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """


        for i in range(0, self.height):
            for j in range(0, self.width):
                cell = (i, j)
                if len(self.moves_made) == (self.height - 1) * (self.width - 1):
                    return None
                if cell not in self.moves_made and cell not in self.mines:
                    self.moves_made.add(cell)
                    return cell
        return None

