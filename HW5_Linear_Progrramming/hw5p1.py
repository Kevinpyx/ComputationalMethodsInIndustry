import scipy.optimize as opt
import numpy as np
import pandas as pd
from IPython.display import display

id12 = np.identity(12)

empty = np.zeros((12,12))

steve = np.identity(12)
steve[1:12, 0:11] = steve[1:12, 0:11] - np.identity(11)

d_i = np.array([440, 550, 820, 777, 915, 920, 790, 666, 748, 441, 546, 718])

A_eq = np.zeros((36,72))
A_eq[0:12,0:12] = -20*id12
A_eq[0:12,12:24] = 1*id12
A_eq[0:12,24:36] = -1*id12
A_eq[12:24,0:12] = 1*steve
A_eq[12:24,36:48] = -1*id12
A_eq[12:24,48:60] = 1*id12
A_eq[24:36,12:24] = -1*id12
A_eq[24:36,60:72] = -1*steve

b_eq = np.zeros((36,))
b_eq[12] = 30
b_eq[24:36] = -d_i
#print(b_eq)

c = np.zeros((72,))
c[:12] = 2000 # w_i
# x_i
c[24:36] = 180 # o_i
c[36:48] = 320 # h_i
c[48:60] = 400 # f_i
c[60:72] = 8 # s_i

A_ub = np.zeros((12,72))
A_ub[0:12, 0:12] = -6*id12
A_ub[0:12, 24:36] = id12

b_ub = np.zeros((12,))

results = opt.linprog(c, A_ub, b_ub, A_eq, b_eq, method='simplex').x
w = results[0:12]
x = results[12:24]
o = results[24:36]
h = results[36:48]
f = results[48:60]
s = results[60:]


dict = {'Month': np.arange(1,13), "Workers": w, "# reg": x, "# overtime": o, 
        'Hire': h, 'Fire': f, 'Stored': s}
df = pd.DataFrame(dict)

display(df)

