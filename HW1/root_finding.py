


def bisect(func, x0, x1, iternum=100, tol=10**(-10)):
    # check for different signs
    f0 = func(x0)
    f1 = func(x1)

    print(f0)
    print(f1)

    if f0*f1 >= 0:
        print("Two points have the same sign.")
        return None
    
    # continue
    m = (x0 + x1)/2
    fm = func(m)

    if iternum == 0 or abs(fm)<tol:
        return m
    
    if fm*f0 < 0:
        return bisect(func, x0, m, iternum-1)
    elif fm*f1 < 0:
        return bisect(func, m, x1, iternum-1)
    else:
        return m



def newton(func, dfunc, x, iternum = 100, tol=10**(-10)):
    fx = func(x)
    dfx = dfunc(x)
    if dfx == 0:
        print("Division by zero")
        return None
    
    print(x)
    #print("fx:", fx)
    #print("dfx:", dfx)
    
    x1 = x - (fx/dfx)


    # base case
    if iternum==0 or x1==x or abs(func(x1))<tol:
        return x1

    # recursive
    return newton(func, dfunc, x1, iternum-1)


def secant(func, x0, x1, iternum=100, tol=10**(-10)):
    f0 = func(x0)
    f1 = func(x1)

    if f0==0:
        return x0
    if f1==0:
        return x1
    
    print(f0)

    diff = f1-f0
    if (diff)==0:
        if x0==x1: # for cases when x0 and x1 converge to the correct root
            return x0
        else: # for cases when x0 and x1 happen to have the same function value
            print("Division by zero")
            return None
    x2 = x1 - f1*(x1-x0)/(diff)

    if iternum==0 or abs(func(x2))<tol:
        return x2

    return secant(func, x1, x2, iternum-1)



