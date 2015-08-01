import os
import sys
from subprocess import call


class SudokuParser(object):

    def __init__(self):
        self.no_of_variables = 0
        self.no_of_clauses = 0

    #Check CommandLine for ouput filename and minisat path
    def get_minisat_path(self):
        try:
            if len(sys.argv[1]) > 1:
                file_name = sys.argv[1]
        except:
            print("No Input File found: Usage: sudoku_parser.py <inputfile> "
                  "<outputfile> <minisatpath>")
            exit(1)
        try:
            if len(sys.argv[2]) > 1:
                outfile = sys.argv[2]
                try:
                    output_file = open(outfile, 'w')
                except:
                    print("Output Filename Invalid: Usage: sudoku_parser.py "
                          "<inputfile> <outputfile> <minisatpath>")
                    exit(1)
        except:
            print("No Output File found: Usage: sudoku_parser.py <inputfile> "
                  "<outputfile> <minisatpath>")
            exit(1)
        try:
            if len(sys.argv[3]) >1:
                minisat_path = sys.argv[3]
        except:
            print("MiniSAT path not found: Usage: sudoku_parser.py <inputfile> "
                  "<outputfile> <minisatpath>")
            exit(1)

        return (file_name, output_file, minisat_path)

    #Gets sudoku puzzle from file and handles wildcard characters
    def get_sudoku_puzzle(self, filename):
  
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


    #Converts value to base 9
    def get_base_nine_num(self, row, col, val):
      
        if val == 0:
            return 0

        digit = 81*(row-1)+9*(col-1)+(val-1)+1
        return digit

    #Creates variable table
    def create_variable_table(self):
    
        rows = '123456789'
        cols = '123456789'
        cells = [row + column for row in rows for column in cols]
        return cells

    #Encodes values from unsolved sudoku
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

    #Decodes SAT output into a tuple (row,col,value)
    def decode(self, val):

        decoded = []
        val -= 1
        num = ((val % 81) % 9)
        col = (((val % 81) - num) / 9)
        row = ((val - col - num) / 81)
        k = int(num + 1)
        j = int(col + 1)
        i = int(row + 1)
        #cell = str(i) + str(j)
        tup = (i, j, k)
        decoded.append(tup)
        return decoded

    #Adds Element clauses to CNF Form
    def element_clauses(self, outputCNFfile):

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
        outputCNFfile.write(line)

    #Adds Row clauses to CNF Form
    def row_clause(self, outputCNFfile):

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
        outputCNFfile.write(line)

    #Adds column clauses to CNF Form
    def column_clause(self, outputCNFfile):

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

    #Adds 3x3 clauses to CNF Form
    def sub_grid_clause(self, output_cnf_file):

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
        output_cnf_file.write(line)

    #Create CNF form to input to MiniSAT
    def create_minisat_input_file(self, tempfile, finalfile):
 
        ln = 'p cnf {var} {clauses}\n'.format(var=self.no_of_variables,clauses=self.no_of_clauses)
        finalfile.write(ln)
        tempfile.flush()
        tempfile.seek(0)
        lines = tempfile.read()
        finalfile.write(lines)
        tempfile.close()
        finalfile.close()

    #Format Output
    def format_output(self, inputFile):

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

    #Output Pretty Sudoku
    def output_sudoku(self, result, outputfile):
     
        decoded = []

        for item in result:
            decoded.extend(sudoku.decode(int(item)))

        sudoku_grid_start = "*---*---*---*---*---*---*---*---*---*\n"
        solved_puzzle = sudoku_grid_start
        cell_counter = 1
        for item in decoded:
            val = item[2]
            if cell_counter % 9 == 0:
                solved_puzzle += '| {} |\n'.format(val)
                solved_puzzle += sudoku_grid_start
                cell_counter += 1
            else:
                solved_puzzle += '| {} '.format(val)
                cell_counter += 1
        outputfile.write(solved_puzzle)

    #Run MiniSAT executable
    def run_minisat(self, inputfile, outputfile, minisatpath):

        try:
            call([minisatpath, inputfile, outputfile,])
        except:
            print("MiniSAT path Invalid: Usage: sudoku_parser.py <inputfile> "
                  "<outputfile> <minisatpath>")
            exit(1)

# File for storing the CNF form
tempinput = open('tempCNF.txt', 'w+')
sudoku = SudokuParser()
filename, outputfile, minisatpath = sudoku.get_minisat_path()
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

#Format Output
result = sudoku.format_output(tempoutput)
sudoku.output_sudoku(result, outputfile)






