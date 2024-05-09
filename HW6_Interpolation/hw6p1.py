import csv
import numpy as np
import pandas as pd

with open('crime_data.csv', mode = 'r') as file:
    csvFile = csv.reader(file)
    crimes = next(file).split(",")[2:9]
    murder = []
    robbery = []
    agasslt = []
    burglry = []
    larceny = []
    mvtheft = []
    arson = []
    population = []
    for line in csvFile:
        if '0' in line:
            pass
        else:
            for i in range(2,10):
                line[i] = int(line[i])
            murder.append(line[2])
            robbery.append(line[3])
            agasslt.append(line[4])
            burglry.append(line[5])
            larceny.append(line[6])
            mvtheft.append(line[7])
            arson.append(line[8])
            population.append(line[9])

murder = np.array(murder)
robbery = np.array(robbery)
agasslt = np.array(agasslt)
burglry = np.array(burglry)
larceny = np.array(larceny)
mvtheft = np.array(mvtheft)
arson = np.array(arson)
population = np.array(population)

def arr2logCol(arr):
    arr = np.log(arr).reshape(-1,1)
    return arr

logpop = arr2logCol(population)
ones = np.ones((len(logpop), 1))
J = np.hstack((logpop, ones))

def linalgSolve(crime):
    crime = arr2logCol(crime)
    a = np.transpose(J)@J
    b = np.transpose(J)@crime
    return np.linalg.solve(a, b)

print(linalgSolve(murder))

lambdas = [linalgSolve(murder)[0],
           linalgSolve(robbery)[0],
           linalgSolve(agasslt)[0],
           linalgSolve(burglry)[0],
           linalgSolve(larceny)[0],
           linalgSolve(mvtheft)[0],
           linalgSolve(arson)[0]]


dict = {'crimes': crimes, 'lambdas': lambdas}
df = pd.DataFrame(dict)
print(df)

"""
While examinig the data, we notice that the number of burglary 
and arson scale linearly with the population. We speculate this 
might be because these are both crimes committed to a property,
and the number of properties in a county should be roughly linearly
proportional to the population.
As for murder, its number scales sublinearly with the population. 
We think this might be because murder is the most serious form of crime 
and there is a higher chance of criminals hesitating because they feel 
being watched by other people.
"""