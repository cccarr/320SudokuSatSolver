__author__ = 'Maryam Lantana'

import os
import sys
from subprocess import call


class SudokuParser(object):

    def __init__(self):
        self.no_of_variables = 0
        self.no_of_clauses = 0

    def get_sudoku_puzzle(self):
        #filename = sys.argv[1]
        filename = 'hard95.txt'
        file = open(filename)
        initial_puzzle = file.readline()
        initial_puzzle = initial_puzzle.strip()
        puzzle = list(initial_puzzle)

        #Handle Wildcards
        for n, item in enumerate(puzzle):
            if item == '.':
                puzzle[n] = '0'
            if item == '?':
                puzzle[n] = '0'
            if item == '*':
                puzzle[n] = '0'	
        #print("".join(puzzle)) #testing
        str_length = len(initial_puzzle)
        #print(str_length) #testing
        return puzzle



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

    def create_variable_table(self):
        rows = '123456789'
        cols = '123456789'
        cells = [row + column for row in rows for column in cols]
        return cells

    def encode(self, puzzle, output_cnf_file):
        table = self.create_variable_table()
        encoded = []
        line = ''
        for n, item in enumerate(puzzle):
            nums = list(table[n])
            i = int(nums[0])
            j = int(nums[1])
            if item == '0':
                continue
            else:
                var = self.get_base_nine_num(i, j, int(item))
                line += '{} 0\n'.format(var)
                self.no_of_clauses += 1
                encoded.append(self.get_base_nine_num(i, j, int(item)))
        output_cnf_file.write(line)
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

    def element_clauses(self, outputCNFfile):
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
        outputCNFfile.write(line)

    def row_clause(self, outputCNFfile):
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
        outputCNFfile.write(line)

    def column_clause(self, outputCNFfile):
        """

        :return:
        """
        line = ''
        for i in range(1, 9):
            for j in range(1, 10):
                for l in range(i+1, 10):
                    line = ''
                    for d in range(1, 10):
                        literal1 = self.get_base_nine_num(i, j, d)
                        literal2 = self.get_base_nine_num(i, l, d)
                        line += '-' + str(literal1) \
                                + ' ' + '-'+str(literal2) \
                                + ' ' + str(0) + '\n'
                    outputCNFfile.write(line)
                    #print(line)

    def sub_grid_clause(self, outputCNFfile):
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

    def run_minisat(self, inputfile, outputfile):
        #TEMP VALUE REPLACE ./Minisat WITH PATH VARIABLE
        #curdir = os.getcwd()
        #minisatexe = curdir + "/MiniSat_v1.14_linux"
        #print(minisatexe)
        #call([minisatexe, inputfile, outputfile,])
        return

# File for storing the CNF form
tempinput = open('tempCNF.txt', 'w')

sudoku = SudokuParser()

puzzle = sudoku.get_sudoku_puzzle()

tempoutput = open('tempSAToutput.txt', 'a')

# Encode Sudoku puzzle and write clauses to CNF File
encoded = sudoku.encode(puzzle, tempinput)
sudoku.element_clauses(tempinput)
sudoku.row_clause(tempinput)
sudoku.column_clause(tempinput)
sudoku.sub_grid_clause(tempinput)

# Run MiniSat to temp output file
sudoku.run_minisat("tempCNF.txt", "tempSAToutput.txt")





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



