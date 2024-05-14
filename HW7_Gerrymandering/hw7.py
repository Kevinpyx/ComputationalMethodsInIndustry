# hw7soln.py
# Eric A. Autry
# CSC 395 Spring 2024
# 05/09/24

import math
import random
import numpy as np
import time
import energy
import gerry

"""
updateBorder: calculates the new border given the old one and the flipped node.

old_border: the old list of border nodes (as row,col) pairs
fliprow: the row of the flipped node
flipcol: the col of the flipped node
plan: the districting plan matrix
N: the size of the plan (NxN)

returns: the new list of border nodes after the node flip is completed,
         the number of ones on the new border,
         the number of zeros on the new border
"""
def updateBorder(old_border, fliprow, flipcol, plan, N):

  # Copy the border.
  new_border = old_border.copy()

  # FIXME - update the new_border!

  # Count the zeros and ones in the new border.
  new_borderOnes, new_borderZeros = gerry.countBorder(new_border, plan)
  if plan[fliprow, flipcol] == 0:
    new_borderOnes += 1
  else:
    new_borderZeros += 1

  return new_border, new_borderOnes, new_borderZeros

"""
calcQ: calculates the value of Q(X->Y) for this problem.
       Note: Q only depends on the current number of border nodes, so we only 
       need to track info related to the current border. But, if we have hit 
       the offset threshold, our choices are more limited. We have separately
       tracked the ones and zeros on the border.

offset: the current offset (#1s-#0s) in the plan
borderOnes: the number of ones on the border
borderZeros: the number of zeros on the border
offset_thresh: the allowable offset threshold

returns: the value of Q(X->Y) for the current step, where the input parameters
         are all defined in terms of X (does not depend on Y)
"""
def calcQ(offset, borderOnes, borderZeros, offset_thresh):
  Q = 0
  #FIXME - calculate Q!
  return Q

"""
metropolis: performs the metropolis sampling.

plan: the initial districting plan matrix (NxN)
offset: the initial offset in the plan (#1s-#0s)
N: the size of the plan (NxN)
offset_thresh: allowable offset threshold

border: the initial list of current border nodes (row,col) pairs
borderOnes: the initial number of ones on the border
borderZeros: the initial number of zeros on the border

measureFunc: the function that calculates mu(X) for metropolis
             measureFunc(plan, border) -> mu

maxIters: the maximum number of metropolis iterations to perform
maxTime: the maximum time to take before stopping iterations (-1 disables)

plotIters: the number of iterations between each plotting point (-1 disables)
filename: the base filename for saving ("" disables plotting)
path: the base path to save to ("" saves with no specified path)
"""
def metropolis(plan, offset, N, offset_thresh, 
               border, borderOnes, borderZeros, 
               measureFunc,
               maxIters=10, maxTime=-1,
               plotIters=-1, filename="", path=""):
  # Set timer for timed runs.
  if maxTime > 0:
    start_time = time.time()

  # Set the initial value of mu, the initial energy.
  mu = measureFunc(plan, border)

  # Plot the initial plan if plotting enabled.
  iter = 0
  if plotIters > 0:
    toprint = ""
    if filename != "":
      fn = filename.split(".")
      fn[0] += "_" + str(iter)
      toprint = ".".join(fn)
      if path != "":
        toprint = path + toprint
      gerry.plotDistrict(plan, toprint)

  # Start the sampling loop.
  timeLimit = math.inf
  if maxTime > 0:
    timeLimit = maxTime + start_time
  while (iter < maxIters) and (time.time() < timeLimit):
    iter += 1

    # FIXME - this is where your Metropolis Implementation goes!

    # Plot if plotIters is set.
    if (plotIters > 0) and (iter%plotIters == 0):
      toprint = ""
      if filename != "":
        fn = filename.split(".")
        fn[0] += "_" + str(iter)
        toprint = ".".join(fn)
        if path != "":
          toprint = path + toprint
        gerry.plotDistrict(plan, toprint)
    
  return plan

"""
Python's "main function" block.
"""
if __name__ == "__main__":

  # Seed the rng. (For reproducible errors.)
  random.seed(110)

  # Set parameters for this trial.
  N = 10 # NxN Matrix
  maxIters = 10000
  maxTime = -1
  offset_thresh = math.floor(N*N/20) # Offset set to ~5%.
  plotIters = 1000

  # Set the plotting info.
  # NOTE:
  #   You can set the filename to be whatever you would like as you test,
  #   but your own name will default to uniform energy. If you use one of
  #   the specified names below, you will activate a specific scenario.
  #   You can feel free to include your own scenarios as well (though you
  #   will need to write those where the energy list is defined below).
  #   Specified filenames:
  #     uniform.png   - will use uniform sampling
  #     left_asym.png - will favor 1s on the left
  #     compact.png   - will maximize compactness
  #     top_left.png  - compactness with 1s in top-left
  filename = "test.png"
  path = "C:\\Users\\eaaut\\Desktop\\Teaching\\395_2024a_spring\\hw7\\"

  # Useful repeated value.
  halfN = math.floor(N/2)

  # Create the initial matrix: vertically split.
  # Also set initial offset (#1s - #0s) as 0 (or +1).
  plan = np.ones((N,N))
  plan[:, :halfN] = 0
  offset = 0
  if (N%2 == 1):
    # Split central column. Center cell = 1.
    plan[:halfN, halfN] = 0
    offset = 1

  # Record the initial border vertices.
  # Store the border vertices as a list of index pairs.
  border = []
  if (N%2 == 0):
    for ii in range(N):
      border.append( (ii, halfN-1) ) # last col of 0s
      border.append( (ii, halfN) )   # last row of 1s
  else:
    for ii in range(halfN):   # split the middle col
      border.append( (ii, halfN) )
      border.append( (ii, halfN+1) )
    for ii in range(halfN,N): # split the middle col
      border.append( (ii, halfN-1) )
      border.append( (ii, halfN) )
  borderOnes, borderZeros = gerry.countBorder(border, plan)

  # Get the energy matrices and set up the energy functions.
  H, V = energy.getHVmatrices(N)
  if filename == "uniform.png":
    energyLst = [(1.0, lambda p,b : 1.0)] # Uniform
  elif filename == "left_asym.png":
    energyLst = [(-1.0, lambda p,b : energy.vert_asym(p, H, V))] # Favor 1s on the left.
  elif filename == "compact.png":
    energyLst = [(1.0, lambda p,b : energy.isoperimetric(p, N, b))] # Compactness.
  elif filename == "top_left.png":
    energyLst = [(-1.0, lambda p,b : energy.vert_asym(p, H, V)), # Favor 1s on the left.
                (-1.0, lambda p,b : energy.horz_asym(p, H, V)), # Favor 1s on the top.
                (1.0, lambda p,b : energy.isoperimetric(p, N, b))] # Compactness.
  else: # default to uniform
    energyLst = [(1.0, lambda p,b : 1.0)] # Uniform
  measureFunc = lambda pp,bb : energy.weightedMu(energyLst, pp, bb)

  # Run the algorithm!
  plan = metropolis(plan, offset, N, offset_thresh, 
                    border, borderOnes, borderZeros, 
                    measureFunc,
                    maxIters, maxTime,
                    plotIters, filename, path)
