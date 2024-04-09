import numpy as np
import hw4
import math
import pickle
import pandas

def isNotInALPHABET(char):
    return not(char in hw4.ALPHABET)


# this function reads the string and saves the value into the transition matrix (ci-nonAlphabet-cj are not considered)
def readIntoMatFreq1(str):
    i = 0
    while(i < len(str) - 1): #
        while(i < len(str)-1 and isNotInALPHABET(str[i])):
            i += 1
        ci = str[i]
        i += 1
        if isNotInALPHABET(str[i]):
            continue # skip the part not in ALPHABET
        else:
            cj = str[i]

        # save it into the matrix
        ind1 = hw4.c2iHelper(ci)
        ind2 = hw4.c2iHelper(cj)
        transitionMatrix[ind1, ind2] += 1




# this function reads the string and saves the value into the transition matrix (ci-nonAlphabet-cj are considered)
def readIntoMatFreq2(str):
    i = 0
    while(i < len(str) - 1): #
        while(i < len(str)-1 and isNotInALPHABET(str[i])):
            i += 1
        ci = str[i]
        i += 1

        while(i < len(str)-1 and isNotInALPHABET(str[i])):
            i += 1

        cj = str[i]

        # save it into the matrix
        ind1 = hw4.c2iHelper(ci)
        ind2 = hw4.c2iHelper(cj)
        transitionMatrix[ind1, ind2] += 1




## main
length = len(hw4.ALPHABET)

transitionMatrix = np.zeros((length, length), dtype=np.double)

print(transitionMatrix)

with open('/Users/kevinpyx/Library/CloudStorage/OneDrive-GrinnellCollege/Grinnell_Documents/Courses/2024_Spring/CSC-395/HW4_Metropolis_Hastings/WarAndPeace.txt') as file:
    data = file.read().replace('\n', '')
    readIntoMatFreq1(data)

transitionMatrixProb = transitionMatrix/np.sum(transitionMatrix)
print(np.sum(transitionMatrix))
#print(transitionMatrixProb)
#print()


transitionMatrixProb[transitionMatrixProb == 0] = math.e**(-20)

# print the transition matrix with pandas in a table
df = pandas.DataFrame(transitionMatrixProb, index=hw4.ALPHABET, columns=hw4.ALPHABET)
print(df)

# Saving the matrix:
with open('transMat.pkl', 'wb') as f: 
    pickle.dump(transitionMatrixProb, f)