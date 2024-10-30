import numpy as np

def score(a, b):
    if(a is None or b is None):
        return -1

    if a == b:
        return 2
    return -1

def distance(a, b):
  matrix = np.zeros((len(a) + 1, len(b) + 1))
  for i in range(1, len(a) + 1):
    for j in range(1, len(b) + 1):
        match = matrix[i-1,j-1] + score(a[i-1], b[j-1])
        delete = matrix[i-1,j] + score(a[i-1], None)
        insert = matrix[i,j-1] + score(None, b[j-1])
        matrix[i,j] = max(match, delete, insert, 0)
  return matrix.max()