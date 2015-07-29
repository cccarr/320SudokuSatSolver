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
        #print("".join(puzzle))
        str_length = len(initial_puzzle)
        #print(str_length)
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
        """

        :param row:
        :param col:
        :param val:
        :return:
        """
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
        """

        :return:
        """
        #print("Element Clauses") # for testing
        line = ''
        for i in range(1, 10):
            for j in range(1, 10):
                for d in range(1, 10):
                    value = self.get_base_nine_num(i, j, d)
                    new_val = '{} '.format(value)
                    line += new_val
                line += '0\n'
        #TODO: Eventually output this to our cnf file
        #print(line) # for testing

    def row_clause(self):
        """

        :return:
        """
        #print("Row Clauses") # for testing
        line = ''
        for i in range(1, 10):
            for j in range(1, 9):
                for l in range(j+1, 10):
                    for d in range(1, 10):
                        literal1 = self.get_base_nine_num(i, j, d)
                        literal2 = self.get_base_nine_num(i, l, d)
                        literals = '-{0} -{1} 0\n'.format(literal1, literal2)
                        line += literals
        #TODO: Eventually output this to our cnf file
        #print(line) # for testing

    def sub_grid_clause(self):
        """

        :return:
        """
        # print("Sub Grid Clauses: ") # for testing
        line = ''
        for d in range(1, 10):
                for a in range(0, 3):
                    for b in range(0, 3):
                        for u in range(1, 4):
                            for v in range(1, 3):
                                for w in range(v+1, 4):
                                    val1 = (3*a) + u
                                    val2 = (3*b) + v
                                    val3 = (3*b) + w
                                    lit1 = self.get_base_nine_num(val1,
                                                                  val2, d)
                                    lit2 = self.get_base_nine_num(val1,
                                                                  val3, d)
                                    literals = "-{0} -{1} 0\n".format(lit1,
                                                                      lit2)
                                    line += literals
        # print("first group: ", line) # for testing

        line = ''
        for d in range(1, 10):
                for a in range(0, 3):
                    for b in range(0, 3):
                        for u in range(1, 3):
                            for v in range(1, 4):
                                for w in range(u+1, 4):
                                    for t in range(1, 4):
                                        val1 = (3*a) + u
                                        val2 = (3*b) + v
                                        val3 = (3*a) + w
                                        val4 = (3*b) + t
                                        lit1 = self.get_base_nine_num(val1,
                                                                      val2, d)
                                        lit2 = self.get_base_nine_num(val3,
                                                                      val4, d)
                                        literals = "-{0} -{1} 0\n".format(
                                            lit1, lit2)
                                        line += literals
        # print("Second group: ", line) # for testing

    def format_output(self, inputFile):
        result = []
        for line in infile:
            lines = line.split(' ')
            for item in lines:
                item = item.strip('\n')
                if item == 'SAT':
                    continue
                if int(item) <= 0:
                    continue
                result.append(int(item))
        return result

sudoku = SudokuParser()

puzzle = sudoku.get_sudoku_puzzle()

#table = sudoku.create_variable_table(puzzle)
sudoku.element_clauses()
sudoku.row_clause()
sudoku.sub_grid_clause()
#base_nine = sudoku.element_clauses()
encoded = sudoku.encode(puzzle)



outfile = open('output.txt', 'w')
for item in encoded:    
    outfile.write(str(item) + ' 0\n')

#Read file
infile = open('exampleoutput.txt', 'r')

result = sudoku.format_output(infile)

#remove negative
#decode

print(result)
decoded = []

for item in result:
     decoded.extend(sudoku.decode(int(item)))

print(decoded)



