
import csv

def penalties_from_csv(csv_filename):
    matrix = dict()
    with open(csv_filename) as csv_fd:
        reader = csv.DictReader(csv_fd, delimiter=';')
        
        for row in reader:
            for i, elem in enumerate(row, 0):
                if i == 0:
                    arg1 = row[elem]
                    matrix[arg1] = dict()
                elif row[elem] != '':
                    matrix[arg1][elem] = int(row[elem])
    return matrix
            

#penalties_from_csv("csvnw.txt")

def reading_from_fasta_file(path_to_file):
    # мб сюда прикрутить автоматическое форматирование к нормальному формату пути
    sequence = ""
    with open(path_to_file, 'r') as f:
        for line in f:
            if line[0] not in [";", ">"]:
                sequence += line.strip()
    return sequence

def making_alignment_matrix(sequence1, sequence2, penalties):
    gap_penalty = 2
    matrix = [[] for i in range(5)]
    matrix[0] = ["start", "gap"]+[letter for letter in sequence1]
    matrix[1] = ["gap", 0]+[gap_penalty*(i+1) for i in range(len(sequence1))]
    for i in range(2, len(sequence2)+2):
        matrix[i] = [sequence2[i-2], gap_penalty*(i-1)] + [0 for i in range(len(sequence1))]
    for i in range(2, len(sequence2)+2):
        for j in range(2, len(sequence1)+2):
            from_left = matrix[i][j-1] + gap_penalty
            from_top = matrix[i-1][j] + gap_penalty
            from_diagonal = matrix[i-1][j-1] + penalties[matrix[0][i]][matrix[j][0]]
            minimum = min(from_diagonal, from_left, from_top)
            matrix[i][j] = [minimum]
            if minimum == from_diagonal:
                matrix.extend([(i-1, j-1)])
            if minimum == from_left:
                matrix.extend([(i, j-1)])
            if minimum == from_top:
                matrix.extend([(i-1, j)])
    return matrix

def searching_best_alignment(matrix):
    pass

def writing_to_fasta_file(path_in_matrix, sequence1, sequence2):
    up_seq = ""
    down_seq = ""
    match = ""
    for number, (i, j) in enumerate(path_in_matrix[1:], 1):
        prev_i, prev_j = path_in_matrix[number-1]
        if prev_i == i:
            up_seq+=sequence1[j-1]
            down_seq += "*"
            match += "*"
        elif prev_j == j:
            down_seq+=sequence2[i-1]
            up_seq += "*"
            match += "*"
        else:
            up_seq+=sequence1[j-1]
            down_seq += sequence2[i-1]
            if sequence1[j-1] == sequence2[i-1]:
                match += "|"
            else:
                match += "x"

    print(up_seq)
    print(match)
    print(down_seq)

#making_alignment_matrix("ABCDEF","XYZ",3)
def main():
    path = [(0,0), (1,1), (2,1), (3,2), (4,3), (4,4), (5,5), (6,6), (7,7), (8,8)]
    writing_to_fasta_file(path, "WJCJGZTE", "WRJCKZTA")
main()