import os


import csv

def penalties_from_csv(csv_filename):
    matrix = dict()
    with open(csv_filename) as csv_fd:
        reader = csv.DictReader(csv_fd, delimiter=',')
        
        for row in reader:
            for i, elem in enumerate(row, 0):
                if i == 0:
                    arg1 = row[elem]
                    matrix[arg1] = dict()
                elif row[elem] != '':
                    matrix[arg1][elem] = int(row[elem])
    return matrix
            

def reading_from_fasta_file(path_to_file):
    # мб сюда прикрутить автоматическое форматирование к нормальному формату пути
    sequence = ""
    with open(path_to_file, 'r') as f:
        for line in f:
            if line[0] not in [";", ">"]:
                sequence += line.strip()
    return sequence

def making_alignment_matrix(sequence1, sequence2, penalties):
    gap_penalty = penalties["*"]["*"]
    matrix = [[] for i in range(len(sequence2)+2)]
    matrix[0] = [["start"], ["gap"]]+[letter for letter in sequence1]
    matrix[1] = [["gap"], [0]]+[[gap_penalty*(i+1), (1, i+1)] for i in range(len(sequence1))]
    for i in range(2, len(sequence2)+2):
        matrix[i] = [sequence2[i-2], [gap_penalty*(i-1), (i-1, 1)]] + [[0] for u in range(len(sequence1))]
    for i in range(2, len(sequence2)+2):
        for j in range(2, len(sequence1)+2):
            
            from_left = matrix[i][j-1][0] + gap_penalty
            from_top = matrix[i-1][j][0] + gap_penalty
            from_diagonal = matrix[i-1][j-1][0] + penalties[matrix[i][0][0]][matrix[0][j][0]]
            minimum = min(from_diagonal, from_left, from_top)
            matrix[i][j] = [minimum]
            if minimum == from_diagonal:
                matrix[i][j].extend([(i-1, j-1)])
            if minimum == from_left:
                matrix[i][j].extend([(i, j-1)])
            if minimum == from_top:
                matrix[i][j].extend([(i-1, j)])
    return matrix

def simple_penalties(sequence1, sequence2):
    alphabet = list(set(sequence1+sequence2))
    penalties = {letter: dict() for letter in alphabet}
    for key in penalties:
        for letter in alphabet:
            if key == letter:
                penalties[key][letter] = -2
            else:
                penalties[key][letter] = 2
    penalties["*"]["*"] = 1
    return penalties

def print_matrix(matrix):

    for i in range(len(matrix)):
        print(" ".join(map(lambda x: str(x).center(5), [elem[0] for elem in matrix[i]])))

def searching_best_alignment(matrix):
    i = len(matrix)-1
    j = len(matrix[i])-1
    path = [(i, j)]

    while not (i==1 and j==1):
        (new_i, new_j) = matrix[i][j][1]
        path.append((new_i, new_j))
        i, j = new_i, new_j
    return path [::-1]

def writing_to_fasta_file(path_in_matrix, sequence1, sequence2, file_path = None):
    up_seq = ""
    down_seq = ""
    match = ""
    for number, (i, j) in enumerate(path_in_matrix[1:], 1):
        prev_i, prev_j = path_in_matrix[number-1]
        if prev_i == i:
            up_seq+=sequence1[j-2]
            down_seq += "*"
            match += "*"
        elif prev_j == j:
            down_seq+=sequence2[i-2]
            up_seq += "*"
            match += "*"
        else:
            up_seq+=sequence1[j-2]
            down_seq += sequence2[i-2]
            if sequence1[j-2] == sequence2[i-2]:
                match += "|"
            else:
                match += "x"
    if file_path is None:
        file_path="alignment.fa"
        print("path", file_path)
    if not os.path.exists(file_path):
        a = open(file_path, "x")
        a.close()
    with open(file_path, "a+") as file:
        file.writelines([">alignment of sequence {} to sequence {}".format(sequence1, sequence2), "\n", up_seq, "\n", match, "\n", down_seq, "\n\n"])
    print(up_seq)
    print(match)
    print(down_seq)

def test1():
    sequence1 = "AATGAACAGT"
    sequence2 = "ATGCACAAGCT"
    penalties = simple_penalties(sequence1, sequence2)
    m = making_alignment_matrix(sequence1, sequence2, penalties)
    print_matrix(m)
    path = searching_best_alignment(m)
    print(path)
    writing_to_fasta_file(path, sequence1, sequence2)

def main():
    print("This program allows you to align pattern to text. To know the list of commands, type 'help'. To quit the program, type 'exit'.")
    possible_commands = ["help", "exit", "input sequences", "input penalties data", "print alignment matrix", "write alignment to file", "find the best alignment"]
    path1, path2, sequence1, sequence2 = "", "", "", ""
    penalties, alignment_matrix = dict(), dict()
    path_in_matrix = []
    while True:
        command = input()
        if command not in possible_commands:
            print("Wrong command. Please try again.")
            continue
        if command == "exit":
            break
        if command == "input sequences":
            print("Write the name of fasta file with sequence 1.")
            path1 = input()
            print("Write the name of fasta file with sequence 2.")
            path2 = input()
            sequence1 = reading_from_fasta_file(path1)
            sequence2 = reading_from_fasta_file(path2)
        if command == "input penalties data":
            print("Write the name of csv file with penalties.")
            csv_filename = input()
            penalties = penalties_from_csv(csv_filename)
        if command == "print alignment matrix":
            if alignment_matrix == dict():
                if sequence1 == "" or sequence2 == "":
                    print("Please input sequences first.")
                    continue
                elif penalties == dict():
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, simple_penalties(sequence1, sequence2))
                else:
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, penalties)
                
            print_matrix(alignment_matrix)
        if command == "write alignment to file":
            if alignment_matrix == dict():
                if sequence1 == "" or sequence2 == "":
                    print("Please input sequences first.")
                    continue
                elif penalties == dict():
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, simple_penalties(sequence1, sequence2))
                else:
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, penalties)
            path_in_matrix = searching_best_alignment(alignment_matrix)
            print("Input the name of the fasta file.")
            file_name = input()
            if file_name == "":
                writing_to_fasta_file(path_in_matrix, sequence1, sequence2)
            else:
                writing_to_fasta_file(path_in_matrix, sequence1, sequence2, file_path)
        if command == "find the best alignment":
            if alignment_matrix == dict():
                if sequence1 == "" or sequence2 == "":
                    print("Please input sequences first.")
                    continue
                elif penalties == dict():
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, simple_penalties(sequence1, sequence2))
                else:
                    alignment_matrix = making_alignment_matrix(sequence1, sequence2, penalties)
            path_in_matrix = searching_best_alignment(alignment_matrix)
        if command == "help":
            print("This is help. The list of possible commands is given below.")
            print("'help': allows you to open Help")
            print("'exit': allows you to quit the program")
            print("'input sequences': allows you to input 2 sequences to align; takes filenames of fasta files with those sequences")
            print("'input penalties data': allows you to input csv file with the substitution matrix; takes filename of csv file")
            print("'print alignment matrix': allows you to print the alignment matrix")
            print("'write alignment to file': allows you to write alignment to the fasta file; takes an optional filename of the fasta file, if not given writes into the file 'alignment.fa'")
            print("'find the best alignment': allows you to find the best alignment")
if __name__ == "__main__":
    main()