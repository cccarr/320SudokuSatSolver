__author__ = 'Maryam Lantana'

import sys


class SudokuParser(object):

    def __init__(self):
        self.var_table = dict()

    def get_sudoku_puzzle(self):
        filename = sys.argv[1]
        #filename = 'hard95.txt'
        print("the file name is:", filename)
        file = open(filename)
        initial_puzzle = file.readline()
        initial_puzzle = initial_puzzle.strip()
        print(initial_puzzle)
        str_length = len(initial_puzzle)
        print(str_length)
        return initial_puzzle

    def create_variable_table(self, puzzle_str):
        rows = '123456789'
        cols = '123456789'
        cells = [row + column for row in rows for column in cols]
        print(cells)
        #for char in puzzle_str:
        return

    def get_base_nine_num(self, row, col, val):
        digit = 81*(row-1)+9*(col-1)+(val-1)+1
        return digit

    def element_clauses(self):
        for i in range(1, 10):
            for j in range(1, 10):
                line = ''
                for d in range(1, 10):
                    value = self.get_base_nine_num(i, j, d)
                    line += str(value) + ' '

                print(line)

    def row_clause(self):
        for i in range(1, 10):
            for j in range(1, 10):
                for l in range(j+1,10):

                    line = ''
                    for d in range(1, 10):
                        value = self.get_base_nine_num(i, j, d)
                        line += str(value) + ' ' + '-'+str

                print(line)

sudoku = SudokuParser()

puzzle = sudoku.get_sudoku_puzzle()

sudoku.create_variable_table(puzzle)
sudoku.element_clauses()


