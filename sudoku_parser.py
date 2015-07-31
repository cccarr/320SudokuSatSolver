__author__ = 'Maryam Lantana'

import os
import sys
from subprocess import call


class SudokuParser(object):

    def __init__(self):
        self.no_of_variables = 0
        self.no_of_clauses = 0

    def get_sudoku_puzzle(self, filename):
        """

        :return:
        """
	try:
            file = open(filename)
        except:
            print("Input Filename Invalid: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
            exit(1)
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
        str_length = len(initial_puzzle)
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
        """

        :return:
        """
        rows = '123456789'
        cols = '123456789'
        cells = [row + column for row in rows for column in cols]
        return cells

    def encode(self, puzzle, output_cnf_file):
        """

        :param puzzle:
        :param output_cnf_file:
        :return:
        """
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
        """

        :param val:
        :return:
        """
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

        :param outputCNFfile:
        :return:
        """
        #print("Element Clauses") # for testing
        line = ''
        for i in range(1, 10):
            for j in range(1, 10):
                for d in range(1, 10):
                    value = self.get_base_nine_num(i, j, d)
                    self.no_of_variables += 1
                    new_val = '{} '.format(value)
                    line += new_val
                line += '0\n'
                self.no_of_clauses += 1
        #print(line) # for testing
        outputCNFfile.write(line)

    def row_clause(self, outputCNFfile):
        """

        :param outputCNFfile:
        :return:
        """
        #print("Row Clauses") # for testing
        line = ''
        for i in range(1, 10):
            for j in range(1, 10):
                for d in range(1, 10):
                    for l in range(j+1, 10):
                        literal1 = self.get_base_nine_num(i, j, d)
                        literal2 = self.get_base_nine_num(i, l, d)
                        literals = '-{0} -{1} 0\n'.format(literal1, literal2)
                        line += literals
                        self.no_of_clauses += 1
        # print(line) # for testing
        outputCNFfile.write(line)

    def column_clause(self, outputCNFfile):
        """

        :param outputCNFfile:
        :return:
        """
        line = ''
        for i in range(1, 10):
            for j in range(1, 10):
                for d in range(1, 10):
                    for l in range(i+1, 10):
                        literal1 = self.get_base_nine_num(i, j, d)
                        literal2 = self.get_base_nine_num(l, j, d)
                        literals = '-{0} -{1} 0\n'.format(literal1, literal2)
                        line += literals
                        self.no_of_clauses += 1
        # print(line)  # for testing
        outputCNFfile.write(line)

    def sub_grid_clause(self, output_cnf_file):
        """

        :param output_cnf_file:
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
                                    self.no_of_clauses += 1
        # print("first group: ", line)  # for testing
        # output_cnf_file.write('first group: \n')
        output_cnf_file.write(line)

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
                                        self.no_of_clauses += 1
        # print("Second group: ", line)  # for testing
        output_cnf_file.write(line)

    def create_minisat_input_file(self, tempfile, finalfile):
        """

        :param tempfile: contains just the cnf clauses
        :param finalfile: contains no. of variables and clauses as well as
        all cnf clauses
        :return: none
        """
        ln = 'p cnf {var} {clauses}\n'.format(var=self.no_of_variables,clauses=self.no_of_clauses)
        finalfile.write(ln)
        tempfile.flush()
        tempfile.seek(0)
        lines = tempfile.read()
        finalfile.write(lines)
        tempfile.close()
        finalfile.close()

    def format_output(self, inputFile):
        """

        :param inputFile:
        :return:
        """
        result = []
        inputFile.flush()
        inputFile.seek(0)
        for line in inputFile:
            lines = line.split(' ')
            for item in lines:
                item = item.strip('\n')
                if item == 'SAT':
                    continue
		if item == 'UNSAT':
                    continue	
                if int(item) <= 0:
                    continue
                result.append(int(item))
        return result

  #  def output_sudoku(self, result):
        """

        :param inputfile:
        :return:
        """
        #remove negative
        #decode

   #     print(result)
    #    decoded = []

     #   for item in result:
      #      decoded.extend(sudoku.decode(int(item))


    def run_minisat(self, inputfile, outputfile, minisatpath):
        """
        Runs the MiniSAT executable
        :param inputfile:   The name of the file that minisat gets input from
        :param outputfile:  The name of the temporary file that minisat outputs to
	:param minisatpath: The path to the minisat executable
        :return:
        """
        try:
            call([minisatpath, inputfile, outputfile,])
        except:
            print("MiniSAT path Invalid: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
            exit(1)
        return

#Check CommandLine for ouput filename and minisat path
try:
    if (len(sys.argv[1]) > 1):
        filename = sys.argv[1]
except:
    print("No Input File found: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
    exit(1)
try:
    if (len(sys.argv[2]) > 1):
        outfile = sys.argv[2]
        try:
            outputfile = open(outfile, 'w')
        except:
            print("Output Filename Invalid: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
            exit(1)
except:
    print("No Output File found: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
    exit(1)
try:
    if (len(sys.argv[3]) >1):
        minisatpath = sys.argv[3]
except:
    print("MiniSAT path not found: Usage: sudoku_parser.py <inputfile> <outputfile> <minisatpath>")
    exit(1)

# File for storing the CNF form
tempinput = open('tempCNF.txt', 'r+')

sudoku = SudokuParser()
puzzle = sudoku.get_sudoku_puzzle(filename)



# Encode Sudoku puzzle and write clauses to CNF File
encoded = sudoku.encode(puzzle, tempinput)
sudoku.element_clauses(tempinput)
sudoku.row_clause(tempinput)
sudoku.column_clause(tempinput)
sudoku.sub_grid_clause(tempinput)

# Create final input file for MiniSat
finalinput = open('FinalCNFClauses.txt', 'w')
sudoku.create_minisat_input_file(tempinput, finalinput)

# Run MiniSat to temp output file
tempoutput = open('tempSAToutput.txt', 'w+')
sudoku.run_minisat("FinalCNFClauses.txt", "tempSAToutput.txt", minisatpath)

#outfile = open('output.txt', 'w')
#for item in encoded:    
#    outputfile.write(str(item) + ' 0\n')
result = sudoku.format_output(tempoutput)

print(result)
decoded = []

for item in result:
    decoded.extend(sudoku.decode(int(item))

#print(decoded)



#sudoku.output_sudoku(result)

#Read file
#infile = open('exampleoutput.txt', 'r')



