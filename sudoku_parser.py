__author__ = 'Maryam Lantana'

import sys


class SudokuParser(object):

    def __init__(self):
        self.var_table = dict()

    def get_sudoku_puzzle(self):
        #filename = sys.argv[1]
        filename = 'hard95.txt'
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
        #TODO KRollans doing this part.
        #TODO: Ensure that wildcard characters ar accounted for.
        #for char in puzzle_str:
        return

    def get_base_nine_num(self, row, col, val):
        """

        :param row:
        :param col:
        :param val:
        :return:
        """
        digit = 81*(row-1)+9*(col-1)+(val-1)+1
        return digit

    def element_clauses(self):
        """

        :return:
        """
        for i in range(1, 10):
            for j in range(1, 10):
                line = ''
                for d in range(1, 10):
                    value = self.get_base_nine_num(i, j, d)
                    line += str(value) + ' '
                line += str(0)
                #TODO: Eventually output this to our cnf file
                #print(line)

    def row_clause(self):
        """

        :return:
        """
        for i in range(1, 10):
            for j in range(1, 9):
                for l in range(j+1, 10):
                    line = ''
                    for d in range(1, 10):
                        value1 = self.get_base_nine_num(i, j, d)
                        value2 = self.get_base_nine_num(i, l, d)
                        line += '-' + str(value1) \
                                + ' ' + '-'+str(value2) \
                                + ' ' + str(0) + '\n'
                    #TODO: Eventually output this to our cnf file
                    #print(line)

    def sub_grid_clause(self):
        """

        :return:
        """
        for d in range(1, 10):
            for a in range(0, 3):
                for b in range(0, 3):
                    for u in range(1, 4):
                        for v in range(1, 3):
                            for w in range(v+1, 4):
                                val1 = (3*a) + u
                                val2 = (3*b) + v
                                base9_value_1 = self.get_base_nine_num(val1,
                                                                       val2, d)
                                val2 = (3*b) + w
                                base9_value_2 = self.get_base_nine_num(val1,
                                                                       val2, d)





sudoku = SudokuParser()

puzzle = sudoku.get_sudoku_puzzle()

sudoku.create_variable_table(puzzle)
sudoku.element_clauses()
sudoku.row_clause()


