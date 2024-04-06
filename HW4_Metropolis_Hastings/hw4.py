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

    message = "As a final note about this exercise, there are no correct or incorrect answers here. Off the top of my head, I can think of over a dozen different approaches to confuse the Metropolis attacker, and I can think of some pros and cons of each. I am not looking for you to find the best method, and it is fine if your method is not able to trick your Metropolis attacker. I am mainly interested in how you think about Metropolis Hastings and how your knowledge of the algorithm has helped shape your ideas here. And remember, this part is supposed to be fun. So have some fun with it."
    cipher = randCipherGen()
    scrambled = encipher(message, cipher)

    #print(transitionMatrix.shape)

    # load transition matrix:
    with open('transMat.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        transitionMatrix = np.array(pickle.load(f))

    #print(transitionMatrix.shape)

    x = randCipherGen()
    bestSol = (x, mu(encipher(scrambled, x)))

    for i in range(10000):
        # print('Round ' + str(i))
        y = nextSol(scrambled, x)
        # print(y)
        prob_y = mu(encipher(scrambled, y))
        if prob_y > bestSol[1]:
            bestSol = (y, prob_y)
        
        x = y

    print(cipher)
    print(x)
    print(encipher(scrambled, x))

    # we are not sure about how we can determine how good a solution is. 
    # It seems the last cipher is not bad (the deciphered message looks like English text a lot),
    # but what's produced from the cipher in bestSol is far worse. 