__author__ = 'Maryam Lantana'

import sys


class SudokuParser(object):

    def __init__(self):
        self.var_table = dict()

    def get_sudoku_puzzle(self):
        #filename = sys.argv[1]
        filename = 'hard95.txt'
        print("the file name is: " + filename)
        file = open(filename)
        initial_puzzle = file.readline()
        initial_puzzle = initial_puzzle.strip()
	puzzle = list(initial_puzzle)
        for n, item in enumerate(puzzle):
            if item == '.':
                puzzle[n] = '0'
        print("".join(puzzle))
        str_length = len(initial_puzzle)
        print(str_length)
        return puzzle

    def create_variable_table(self, puzzle_str):
        rows = '123456789'
        cols = '123456789'
        cells = [row + column for row in rows for column in cols]
        #print(cells)
        #TODO: Ensure that wildcard characters ar accounted for.
        #for char in puzzle_str:
        return cells

    def get_base_nine_num(self, row, col, val):
        if val == 0:
            return 0
        digit = 81*(row-1)+9*(col-1)+(val-1)+1
        return digit
    
    def encode(self, puzzle):
        table = sudoku.create_variable_table(puzzle)
	encoded = []
        for n, item in enumerate(puzzle):
            nums = list(table[n])
            i = int(nums[0])
            j = int(nums[1])
            if item == '0':
                continue
            encoded.append(sudoku.get_base_nine_num(i, j, int(item)))
        return encoded

    def decode(self, val):
        decoded = []
        val = val - 1
        num = ((val % 81) % 9)
        col = (((val % 81) - num) / 9)
        row = ((val - col - num) / 81)
	k = num + 1
	j = col + 1
        i = row + 1
        cell = str(i) + str(j)  
	decoded.append(cell)
	decoded.append(k)
        return decoded

    def element_clauses(self):
        line = ''
        for i in range(1, 10):
            for j in range(1, 10):
                for d in range(1, 10):
                    value = self.get_base_nine_num(i, j, d)
                    line += str(value) + ' '
                line += str(0)
                print(line)

    def row_clause(self):
        line = ''
        for i in range(1, 10):
            for j in range(1, 9):
                for l in range(j+1,10):
                    line = ''
                    for d in range(1, 10):
                        value1 = self.get_base_nine_num(i, j, d)
                        value2 = self.get_base_nine_num(i, l, d)
                        line += '-' + str(value1) \
                                + ' ' + '-'+str(value2) \
                                + ' ' + str(0) + '\n'
                    #Put value in cnf file to be fed to minisat here
                    print(line)

sudoku = SudokuParser()

puzzle = sudoku.get_sudoku_puzzle()

table = sudoku.create_variable_table(puzzle)
sudoku.row_clause()
base_nine = sudoku.element_clauses()
encoded = sudoku.encode(puzzle)



outfile = open('output.txt', 'w')
for item in encoded:    
    outfile.write(str(item) + ' 0\n')
print(encoded)
decoded = []
for item in encoded:
     decoded.extend(sudoku.decode(int(item)))

print(decoded)



