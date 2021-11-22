def get_input():
    A = input()
    B = input()
    return A,B

def create_table(A,B):
    path = {}
    table = [[0] * (len(A) + 1)]
    for i in range(len(B)):
        table.append([0] * (len(A) + 1))
    a = len(A)
    b = len(B)
    miss = 1
    gap = 2
    allign = -1
    if (A[1] == B[1]):
        table[1][1] = allign
    else:
        table[1][1] = miss

    for i in range(a):
        table[0][i + 1] = table[0][i] + gap
        n = {(0, i + 1): (0, i)}
        path.update(n)

    for j in range(b):
        n = {(j + 1, 0): (j, 0)}
        path.update(n)
        table[j + 1][0] = table[j][0] + gap

    for i in range(1, b + 1):
        for j in range(1, a + 1):
            n = {(i, j): []}
            path.update(n)
            if A[j - 1] == B[i - 1]:
                table[i][j] = min(table[i - 1][j - 1] + allign, table[i - 1][j] + gap, table[i][j - 1] + gap)

                if table[i][j] == table[i - 1][j - 1] + allign:
                    path[(i, j)].append((i - 1, j - 1))

                if table[i][j] == table[i][j - 1] + gap:
                    path[(i, j)].append((i, j - 1))

                if table[i][j] == table[i - 1][j] + gap:
                    path[(i, j)].append((i - 1, j))

            else:
                table[i][j] = min(table[i - 1][j - 1] + miss, table[i - 1][j] + gap, table[i][j - 1] + gap)

                if table[i][j] == table[i - 1][j - 1] + miss:
                    path[(i, j)].append((i - 1, j - 1))

                if table[i][j] == table[i][j - 1] + gap:
                    path[(i, j)].append((i, j - 1))

                if table[i][j] == table[i - 1][j] + gap:
                    path[(i, j)].append((i - 1, j))

    """ table = [[0] * (len(A))]
    for i in range(len(B) - 1):
        table.append([0] * (len(A)))

    a = len(A)
    b = len(B)

    miss = 1
    gap = 2
    allign = -1

    if (A[0] == B[0]):
        table[0][0] = allign
    else:
        table[0][0] = miss

    for i in range(a - 1):
        table[0][i + 1] = table[0][i] + gap

    for j in range(b - 1):
        table[j + 1][0] = table[j][0] + gap

    for i in range(1, b):
        for j in range(1, a):
            if A[j] == B[i]:
                table[i][j] = min(table[i - 1][j - 1] + allign, table[i - 1][j] + gap, table[i][j - 1] + gap)
            else:
                table[i][j] = min(table[i - 1][j - 1] + miss, table[i - 1][j] + gap, table[i][j - 1] + gap)
"""
    return table,path

def reverse_assembly(table, path,A,B):
    i = len(B)
    j = len(A)
    answer = ''
    score = 0
    miss = 1
    gap = 2
    allign = -1

    def search(table, i, j, answer, score):
        check1 = 100000000000
        check2 = 100000000000
        check3 = 100000000000
        check4 = 100000000000
        if i != 0 and j != 0:
            if table[i - 1][j - 1] in path.get((i, j)):
                check1 = table[i - 1][j - 1] + allign
            if table[i - 1][j - 1] in path.get((i, j)):
                check2 = table[i - 1][j - 1] + miss
            if table[i - 1][j] in path.get((i, j)):
                check3 = table[i - 1][j] + gap
            if table[i - 1][j] in path.get((i, j)):
                check4 = table[i - 1][j] + gap

            further = min(check3, check4, check2, check1)
            if table[i][j] == table[i - 1][j - 1] + allign and (i - 1, j - 1) in path.get((i, j)) and further == check1:
                answer += 'C'
                score += table[i][j]
                return search(table, i - 1, j - 1, answer, score)

            if table[i][j] == table[i - 1][j - 1] + miss and (i - 1, j - 1) in path.get((i, j)) and further == check2:
                answer += 'M'
                score += table[i][j]
                return search(table, i - 1, j - 1, answer, score)

            if table[i][j] == table[i - 1][j] + gap and (i - 1, j) in path.get((i, j)) and further == check4:
                answer += '1G'
                score += table[i][j]
                return search(table, i - 1, j, answer, score)

            if table[i][j] == table[i][j - 1] + gap and (i, j - 1) in path.get((i, j)) and further == check3:
                answer += '2G'
                score += table[i][j]
                return search(table, i, j - 1, answer, score)

        if i == 0 and j != 0:
            if table[i][j] == table[i][j - 1] + gap:  # and (i,j-1) in path.get((i,j)):
                answer += '2G'
                score += table[i][j]
                return search(table, i, j - 1, answer, score)

        if i != 0 and j == 0:
            if table[i][j] == table[i - 1][j] + gap and (i - 1, j) in path.get((i, j)):
                answer += '1G'
                score += table[i][j]
                return search(table, i - 1, j, answer, score)

        else:
            if table[0][0] == 1:
                #answer += "M"
                score += table[i][j]
            else:
                #answer += "C"
                score += table[i][j]
            return answer[::-1], score

    return search(table,i,j,answer,score)


if __name__ == "__main__":
    A,B = get_input()
    table,path = create_table(A,B)
    compare_and_lenght = reverse_assembly(table,path,A,B)

    for i in table:
        print(i)

    print(compare_and_lenght)