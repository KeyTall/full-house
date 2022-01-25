def fullhouse(d_1: int, d_2: int, d_3: int, d_4: int, d_5: int) -> bool:
    '''
    Determins if a roll is a full house out of 5 dice.
    
    Full House: 3 die are the same and the other 2 die are the same. But cannot 
                be 5 of the same.
    
    >>> fullhouse(1,1,1,2,2)
    True
    >>> fullhouse(1,3,3,2,2)
    False
    >>> fullhouse(2,2,2,2,2)
    False
    '''
    dice    = [d_1, d_2, d_3, d_4, d_5]
    count_2 = False
    count_3 = False
    
    num_set_3  = 0
    count      = 1
    origin     = dice[0] #First Term in list
    
    for i in range(4):
        #Term i in dice list switches with first Term in list
        dice [0] = dice[i]
        dice [i] = origin
        
        #Counts repeated numbers
        for num in range(1,5):
            if dice[0] == dice[num]:
                count += 1
                
        #3 numbers are the same
        if count == 3:
            num_set_3 = dice[0]
            count_3   = True
        #2 numbers are the same and are not the same numbers as the other 3
        elif dice[0] != num_set_3 and count == 2:
            count_2 = True
            
        count = 1
    
    #If found 2 and 3 numbers the same returns True
    if count_2 and count_3:
        result = True
   #If not found 2 and 3 numbers the same returns False
    else:
        result = False
        
    return result

fullhouse(1,1,1,2,2)

