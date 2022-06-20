"""
File: Peg_Solitare.py
Author: Christopher Kihano
Date: June 20 2022
Description: Solver for peg solitaire game in a triangle format. Can create triangle boards that are triangle with
             length n and any initial board configuration. Inspired by the peg solitaire game at Cracker Barrel.
Further Improvements: Optimizations may include detection for symmetry to reduce computation. For example, in the
                      default setup, there are two possible initial moves but they're symmetrical of each other. Any
                      solution of one would be a mirror copy of the other reducing the number of iterations by half.

                      Allowing for additional layouts of boards including a cross, triangle without tips, stars. These
                      would require either additional equations to find valid moves or hardcoded boards.
"""

import copy
import time


class Board:
    """Peg board layout for a triangle shaped board with sides of length n."""
    def __init__(self, n: int):
        self.size = n
        # Find the total num of holes. Notes: Triangle numbers, Gauss
        # This is useful for one line later on in this script but in other languages where we need to set the size
        #   of an array, we need to know how much memory we need to allocate for a board.
        self.numHoles = (n**2 + n) // 2
        self.holes = list()
        self.winSize = self.numHoles - 2
        # For a given board instance, this is the route that it's taken so far.
        self.route = list()
        # Pos is used so that we don't need to recalculate where a given peg should be in the board given the row and
        #   offset.
        pos = 0
        for row in range(n):
            for offset in range(row+1): # row+1 because when row = 0, range(0) does not produce a loop
                self.holes.append(Hole(n, pos, row, offset))
                pos += 1

    def valid_moves(self):
        """Finds all valid moves for a given board state."""
        moves = list()
        # A list comprehension could be used here but would produce less readable code. Works fine as is.
        for hole in self.holes:
            if hole.has_peg:
                for move in hole.moves:
                    if self.holes[move[0]].has_peg and not self.holes[move[1]].has_peg:
                        moves.append([hole.pos, move[0], move[1]])
        return moves


class Hole:
    """
    Hole is used for keeping track of if a peg is in the hole and the possible moves a peg in that location could make.
    """
    def __init__(self, n: int, pos: int, row: int, offset: int):
        self.pos = pos
        self.has_peg = True  # Always set to true initially, allow for program to set for missing pegs afterwards.
        self.moves = list()
        if offset-row < -1:  # Can a move be played to the east and northeast?
            self.moves.append([pos+1, pos+2])
            self.moves.append([pos-row, pos-2*row+1])
        if offset > 1:  # Can a move be played to the west and northwest?
            self.moves.append([pos-1, pos-2])
            self.moves.append([pos-row-1, pos-2*row-1])
        if n-row > 2:  # Can a move be played to the south?
            self.moves.append([pos+row+1, pos+2*(row+1)+1])
            self.moves.append([pos+row+2, pos+2*(row+1)+3])


def find_solutions(board, show_solutions=True):
    """Iterates using a tree structure to find all solutions for the given initial board. """
    find_solutions.num_of_function_runs += 1
    moves = board.valid_moves()
    if len(moves) == 0:  # If there are no valid moves, no actions can be taken.
        return
    for move in moves:
        new_board = copy.deepcopy(board)
        # Add move to log
        new_board.route.append([move[0], move[2]])
        # Perform move
        new_board.holes[move[0]].has_peg = False
        new_board.holes[move[1]].has_peg = False
        new_board.holes[move[2]].has_peg = True
        # Check if end has been reached
        if len(new_board.route) == new_board.winSize:
            if show_solutions:
                print(new_board.route)  # Shows the most recent solution
            #print(find_solutions.num_of_solutions)  # Uncomment to ensure script is finding solutions, not stalled
            find_solutions.num_of_solutions += 1
            return
        # Try new board
        find_solutions(new_board)
    return


if __name__ == '__main__':
    startTime = time.time()
    # Initialize a 5-sided board
    tempBoard = Board(5)
    # Remove the peg indicated by the instructions
    tempBoard.holes[0].has_peg = False
    # Begin solving
    find_solutions.num_of_solutions = 0
    find_solutions.num_of_function_runs = 0
    find_solutions(tempBoard, True)
    endTime = time.time()
    print(find_solutions.num_of_solutions)
    print(find_solutions.num_of_function_runs)
    print(endTime-startTime)
