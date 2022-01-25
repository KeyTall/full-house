A = 10
B = 11
C = 12
D = 13
E = 14
F = 15

def base_n_to_base_10(n: int, x1,x2,x3,x4) -> None:
    ''''
    -Converts base number to base-10
    -n is base you are converting from
    -x1 through x4 are digits of counting system
    
    Precondition: Goes up to base-16 and lowest base-2.
    
    >>> base_n_to_base_10(2, 1,0,1,1)
    11
    >>> base_n_to_base_10(16, A,F,3,7)
    44855
    >>> base_n_to_base_10(17, 9,1,3,7)
    Range of Bases is 2-16
    >>> base_n_to_base_10(10, 2,7,7,7)
    2777
    ''' 
    
    if n > 16 or n < 2:
        print('Range of Bases is 2-16')
    elif n == 10:
        print(str(x1) + str(x2) + str(x3) + str(x4))
    else:           
        y1 = x1 * n + x2
        y2 = y1 * n + x3
        y3 = y2 * n + x4
    
        print(y3)

