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
        return ord(char) - 65 + 26
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
    if (logSumY - logSumX) > 10: #so that there won't be an overflown error due to the index being too big
        accProb = 1
    else: 
        accProb = math.e**(logSumY - logSumX)
        accProb = min(accProb, 1)


    # determine to accept or not
    if rand.random() <= accProb:
        return y
    return x

# This function computes the log of mu(x) of a message so that we can compare how good a solution is
# We tried exponentiate the log but then all the probability are too small to compare
def logMu(message):
    i = 0
    logSum = 0
    while (i < len(message)-1):
        ci = message[i]
        cj = message[i+1]
        prob = transitionMatrix[c2iHelper(ci)][c2iHelper(cj)]
        logSum += math.log(prob)
        i += 1

    # print(logSum)
    return logSum # was originally math.e**(logSum), but we found this works better


if __name__ == "__main__":

    message = "As a final note about this exercise, there are no correct or incorrect answers here. Off the top of my head, I can think of over a dozen different approaches to confuse the Metropolis attacker, and I can think of some pros and cons of each. I am not looking for you to find the best method, and it is fine if your method is not able to trick your Metropolis attacker. I am mainly interested in how you think about Metropolis Hastings and how your knowledge of the algorithm has helped shape your ideas here. And remember, this part is supposed to be fun. So have some fun with it."
    cipher = randCipherGen()
    scrambled = encipher(message, cipher)

    #print(transitionMatrix.shape)

    # load transition matrix:
    with open('/Users/kevinpyx/Library/CloudStorage/OneDrive-GrinnellCollege/Grinnell_Documents/Courses/2024_Spring/CSC-395/HW4_Metropolis_Hastings/transMat.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        transitionMatrix = np.array(pickle.load(f))

    #print(transitionMatrix.shape)
'''
    x = randCipherGen()
    bestSol = (x, logMu(encipher(scrambled, x)))

    for i in range(20000):
        y = nextSol(scrambled, x)
        # print(y)
        prob_y = logMu(encipher(scrambled, y))
        
        if prob_y > bestSol[1]:
            bestSol = (y, prob_y)
        
        x = y

    # print(cipher)
    print(bestSol[0])
    print(encipher(scrambled, bestSol[0]))
    print('bestSol logProb: ' + str(logMu(encipher(scrambled, bestSol[0]))))
'''
    

'''
Part 2:
Method 1:
After every letter, we can insert a character that comes after this character in the alphabet sequence (or whatever character).
e.g. "bad" -> "bcabde"

Method 2:
Reverse the message
e.g. "bad" -> "dab"

Maximum Security: when pushed to their extremes, which method do you think will be able to provide the highest level of security?
- We think the first method might be able to provide the highest level of security when pushed to extreme because it changes the length of the message and decreases the probability of the message being generated by the transition matrix.
Efficient Security: which method provides the greatest amount of increased security for the least amount of work?
- Reversing the message requires a lot less work than method 1, so we think this method is more efficient.

'''
# The sender can use this function to insert the characters after each character in the original message
def insert(msg):
    str = ''
    for char in msg:
        i = c2iHelper(char)
        if (i == length - 1):
            str = str + char + ALPHABET[0]
        else:
            str = str + char + ALPHABET[i+1]
    return str

# The receiver can use this function to remove the inserted characters
def remove(msg):
    str = ''
    for i in range(len(msg)):
        if i%2 == 0:
            str = str + msg[i]
    return str

if __name__ == "__main__":

    # sender:
    processed = insert(message)
    scrambled = encipher(processed, cipher)

    # attacker without remove function:
    x = randCipherGen()
    bestSol = (x, logMu(encipher(scrambled, x)))

    for i in range(20000):
        y = nextSol(scrambled, x)
        # print(y)
        prob_y = logMu(encipher(scrambled, y))
        
        if prob_y > bestSol[1]:
            bestSol = (y, prob_y)
        
        x = y

    # print(cipher)
    print(bestSol[0])
    print(encipher(scrambled, bestSol[0]))
    print('bestSol logProb: ' + str(logMu(encipher(scrambled, bestSol[0]))))




    # receiver with remove function:
    scrambled = remove(scrambled)
    x = randCipherGen()
    bestSol = (x, logMu(encipher(scrambled, x)))

    for i in range(20000):
        y = nextSol(scrambled, x)
        # print(y)
        prob_y = logMu(encipher(scrambled, y))
        
        if prob_y > bestSol[1]:
            bestSol = (y, prob_y)
        
        x = y

    # print(cipher)
    print(bestSol[0])
    print(encipher(scrambled, bestSol[0]))
    print('bestSol logProb: ' + str(logMu(encipher(scrambled, bestSol[0]))))