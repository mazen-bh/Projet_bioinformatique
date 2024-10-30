import numpy as np

def distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = matrix[i-1,j-1] + (0 if seq1[i-1] == seq2[j-1] else 1)
            delete = matrix[i-1,j] + 1
            insert = matrix[i,j-1] + 1
            matrix[i,j] = min(match, delete, insert)
    return matrix[size_x - 1, size_y - 1]