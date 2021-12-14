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
        self.mines = set()

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
        self.mines_found = set()

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


class Sentence():
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
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

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
        add_sentences = []

        cells, count = self.new_sentence_from_move(cell, count)
        
        new_sentence = Sentence(cells,count)
        add_sentences.append(new_sentence)

        # Repeat this loop until we might possibly have new connections: we repeat if we add any new info anytime
        repeat = True
        while repeat:
            repeat = False
            # new_sentences is just a holder so we don't mutate our list on the flow
            new_sentences = []
            for add_sentence in add_sentences:
                # Add new base knowledges
                if add_sentence not in self.knowledge:
                    self.knowledge.append(add_sentence)
                    repeat = True
                # Check if there are possible supersets in any way, if there are we add the new knowledge from it
                for sentence in self.knowledge:
                    if sentence.cells < add_sentence.cells:
                        new_sentence = Sentence(set(add_sentence.cells - sentence.cells), add_sentence.count - sentence.count)
                        if new_sentence not in self.knowledge:
                            new_sentences.append(new_sentence)
                            self.knowledge.append(new_sentence)
                            repeat = True
                    elif sentence.cells > add_sentence.cells:
                        new_sentence = Sentence(set(sentence.cells - add_sentence.cells), sentence.count - add_sentence.count)
                        if new_sentence not in self.knowledge:
                            new_sentences.append(new_sentence)
                            self.knowledge.append(new_sentence)
                            repeat = True
            add_sentences = new_sentences

            repeat = self.update_knowledge()

            self.delete_used_sentences()
            


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for row in range(self.width):
            for column in range(self.height):
                if (row,column) not in self.moves_made:
                    if (row,column) not in self.mines:
                        return (row,column)


    def new_sentence_from_move(self,cell, count):
        """
        Returns a set of cells and mine count for the new sentence.
        Only take into account cells that have not been chosen, or otherwise are not known to be safe.
        """
        cells = set()
        for row_counter in range(max(0,cell[0]-1), min(cell[0]+2,self.height)):
            for column_counter in range(max(0,cell[1]-1), min(cell[1]+2,self.width)):
                if (row_counter,column_counter) not in self.moves_made:
                        if (row_counter,column_counter) not in self.safes:
                            if (row_counter,column_counter) not in self.mines:
                                cells.add((row_counter,column_counter))
                            else: 
                                count -= 1
        return (cells,count)

    def update_knowledge(self):
        """
        Update our knowledges if possible: all mines or all safe.
        Repeat loop until we can't update once
        Return true if we updated at least once, false otherwise
        """
        did_we_update = False
        is_knowledge_possibly_updatable = True

        while is_knowledge_possibly_updatable:
            is_knowledge_possibly_updatable = False
            new_safes = set()
            new_mines = set()
            for sentence in self.knowledge:
                if sentence.count <= 0:
                    did_we_update = True
                    for cell in sentence.cells:
                        new_safes.add(cell)
                elif sentence.count == len(sentence.cells):
                    did_we_update = True
                    is_knowledge_possibly_updatable = True
                    for cell in sentence.cells:
                        new_mines.add(cell)

            for cell in new_safes:
                self.mark_safe(cell)

            for cell in new_mines:
                self.mark_mine(cell)
        return did_we_update

    def delete_used_sentences(self):
        """
        If we know a sentence is safe or mines, we can delete it from knowledge.
        This comes after we updated every other knowledge about it.
        """
        delete_sentences = []
        for sentence in self.knowledge:
            if sentence.count <= 0 or sentence.count == len(sentence.cells):
                delete_sentences.append(sentence)
            
        for sentence in delete_sentences:
            self.knowledge.remove(sentence)

        new_knowledge = []
        for sentence in self.knowledge:
            if sentence not in new_knowledge:
                new_knowledge.append(sentence)
        self.knowledge = new_knowledge