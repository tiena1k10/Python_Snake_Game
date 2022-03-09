sankes = [[6,6],[6,7],[6,8]]

def min_Path(a,b):
    for i in range(840*840):
        for j in range(840*840):
            if [i,j] in sankes:
                matrix[i][j] = 9999;
            else:
                matrix[i][j] = 1;
    for i in range(840*840):
        arr[i] = matrix[a][i]
        