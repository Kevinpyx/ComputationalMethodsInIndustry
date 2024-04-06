import random as rand
import numpy as np
import pickle
import math

lowercase = [chr(i) for i in range(97, 123)]
uppercase = [chr(i) for i in range(65, 91)]
special = [' ', ',', '.']
ALPHABET = lowercase + uppercase + special

length = len(ALPHABET)
transitionMatrix = np.zeros((length, length), dtype=np.double)

# converts a character in the alphabet to its index
# precondition: char has to be a character in the alphabet
def c2iHelper(char):
    if char.islower():
        return ord(char) - 97
    elif char.isupper(): 
        return ord(char) - 65
    elif char == ' ':
        return 52
    elif char == ',':
        return 53
    elif char == '.':
        return 54
    else:
        raise Exception("Element not in ALPHABET")

# randCipherGen(): It generates a random cipher by sampling the alphabets
def randCipherGen():
    return rand.sample(ALPHABET, len(ALPHABET))

# encipher(msg, cipher): ciphers the msg with the cipher provided
# msg: String, a text message
# cipher: list of alphabets
def encipher(msg, cipher):
    ciphered = ''
    for char in msg:
        ind = c2iHelper(char)
        ciphered += cipher[ind]
    return ciphered

def swap(cipher):
    y = cipher.copy()
    i1 = rand.randint(0, length-1)
    i2 = rand.randint(0, length-1)
    temp = y[i1]
    y[i1] = y[i2]
    y[i2] = temp
    return y


# returns the next solution from current solution. If the next solution is the same with the current one, it means the new solution is not accepted
def nextSol(encrypted, x):
    y = swap(x) # propose next solution

    # try to decipher the message with both ciphers
    decryptX = encipher(encrypted, x)
    decryptY = encipher(encrypted, y)

    # calculate the log sums
    i = 0
    logSumX = 0
    while (i < len(decryptX)-1):
        ci = decryptX[i]
        cj = decryptX[i+1]
        prob = transitionMatrix[c2iHelper(ci)][c2iHelper(cj)]
        logSumX += math.log(prob)
        i += 1

    i = 0
    logSumY = 0
    while (i < len(decryptY)-1):
        ci = decryptY[i]
        cj = decryptY[i+1]
        prob = transitionMatrix[c2iHelper(ci)][c2iHelper(cj)]
        logSumY += math.log(prob)
        i += 1
    
    # compute the acceptance probability
    accProb = math.e**(logSumY - logSumX)
    
    accProb = min(accProb, 1)

    # determine to accept or not
    if rand.random() <= accProb:
        return y
    return x

def mu(message):
    i = 0
    logSum = 0
    while (i < len(message)-1):
        ci = message[i]
        cj = message[i+1]
        prob = transitionMatrix[c2iHelper(ci)][c2iHelper(cj)]
        logSum += math.log(prob)
        i += 1

    return math.e**(logSum)


if __name__ == "__main__":

    message = "As a final note, remember that this method is random, so it might fail to decipher the text even if implemented correctly. If it fails, try again several times. You should be able to decipher the message most of the time, so a few attempts should be sufficient."
    cipher = randCipherGen()
    scrambled = encipher(message, cipher)

    print(transitionMatrix.shape)

    # load transition matrix:
    with open('transMat.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        transitionMatrix = np.array(pickle.load(f))

    print(transitionMatrix.shape)

    x = randCipherGen()
    bestSol = (x, mu(encipher(scrambled, x)))

    for i in range(10000):
        # print('Round ' + str(i))
        y = nextSol(scrambled, x)
        prob_y = mu(encipher(scrambled, y))
        if prob_y > bestSol[1]:
            bestSol = (y, prob_y)
        
        x = y

    print(x)
    print(encipher(scrambled, x))