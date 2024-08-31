#Part 1: A bit random
import random

DEF_DIFFIC = 10
MAX_TRIALS = 20
MAX_VALUE = 99
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
DIGITS2 = "123456789"
NOT_POSSIBLE = "No FoCdle found of that difficulty"

def create_secret(difficulty=DEF_DIFFIC):
    '''
    Use a random number function to create a FoCdle instance of length 
    `difficulty`. The generated equation will be built around three values 
    each from 1 to 99, two operators, and an equality.
    '''
    trials = 0
    while trials < MAX_TRIALS:
        # Generate 3 random numbers 
        num_list = []
        for num in range(3):
            if difficulty <= 8:
                num_list.append(str(random.choice(DIGITS)))
            else:
                num_list.append(str(random.randint(1, MAX_VALUE + 1)))
        
        # Generate 2 random operators 
        op_list = []
        for op in range(2):
            oper = random.choice(OPERATORS)
            op_list.append(oper)
            
        # No leading 0 allowed 
        for digit in range(len(num_list)):
            if num_list[digit] == '0':
                num_list[digit] = str(random.choice(DIGITS2))
                
        # Make new list containing the numbers and operators  
        equation_list = [num_list[0], op_list[0], num_list[1], op_list[1],
                         num_list[2]]
        # Checking whether there is '%0' as it could lead to an error 
        for sym in range(len(equation_list)):
            if equation_list[sym] == '%' and equation_list[sym + 1] == '0':
                equation_list[sym + 1] = str(random.choice(DIGITS2))
        equation = ''.join(equation_list)
        result = eval(equation)
        full_equation = f"{equation}{EQUALITY}{result}"
    
        if len(full_equation) != difficulty or result <= 0:
            trials += 1
        else:
            return full_equation

    return NOT_POSSIBLE 
        
#Part 2: Setting Colors 
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"

def set_colors(secret, guess):
    '''
    Compares the latest `guess` equation against the unknown `secret` one. 
    Returns a list of three-item tuples, one tuple for each character position 
    in the two equations:
        -- a position number within the `guess`, counting from zero;
        -- the character at that position of `guess`;
        -- one of "green", "yellow", or "grey", to indicate the status of
           the `guess` at that position, relative to `secret`.
    The return list is sorted by position.
    '''
    green_list = []
    y_g_list = []  # For yellows and greys only 
    
    # Seperating the greens with the yellows and greys
    for index in range(len(guess)):
        g_current = guess[index]
        s_current = secret[index]
        if g_current == s_current:
            green_list.append((index, g_current, GREEN))
        else:
            y_g_list.append((index, g_current))

    for i, char in y_g_list:
        # Creating a dictionary of the char and number of green char
        # Or the number of color-assigned char 
        secret_count = {}
        for idx, chara, colour in green_list:
            if chara in secret_count:
                secret_count[chara] += 1
            else:
                secret_count[chara] = 1
        
        # To check whether the color for char in y_g_list be yellow or grey
        if char in secret and char in secret_count:
            remaining = secret.count(char) - secret_count[char]
            if remaining == 0:
                green_list.append((i, char, GREYY))
            elif remaining < 0:
                green_list.append((i, char, GREYY))
            else:
                green_list.append((i, char, YELLO))
                
        elif char in secret and char != secret[i]:
            green_list.append((i, char, YELLO))
            
        else:
            green_list.append((i, char, GREYY))

    return sorted(green_list)
    
#Part 3: Checking Restrictions 
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"

def passes_restrictions(guess, all_info):
    '''
    Tests a `guess` equation against `all_info`, a list of known restrictions, 
    one entry in that list from each previous call to set_colors(). Returns 
    True if that `guess` complies with the collective evidence imposed by 
    `all_info`; returns False if any violation is detected. Does not check the 
    mathematical accuracy of the proposed candidate equation.
    '''
    green_list = []
    yellow_dict = {}
    grey_list = []
    
    if all_info == []:
        return True 
    
    for row in all_info:
        row_yellow_chars = []
        for index, char, color in row:
            if color == GREEN:
                if (index, char) in green_list:
                    continue
                else:
                    green_list.append((index, char))
            # Creating a dictionary containing number of char and its indexes
            # That are not green 
            elif color == YELLO:
                if char in yellow_dict:
                    if char in row_yellow_chars:
                        count = yellow_dict[char][0]  # num of char in secret
                        index_list = yellow_dict[char][1]
                        count += 1
                        index_list.append(index)
                        yellow_dict[char] = [count, index_list] 
                    else:
                        count = yellow_dict[char][0]
                        index_list = yellow_dict[char][1]
                        if index not in index_list:
                            index_list.append(index)
                            yellow_dict[char] = [count, index_list]
                        else:
                            continue
                else:
                    index_list = []
                    index_list.append(index)
                    yellow_dict[char] = [1, index_list]
                row_yellow_chars.append(char)
            elif color == GREYY:
                if char in yellow_dict:
                    count = yellow_dict[char][0]
                    index_list = yellow_dict[char][1]
                    index_list.append(index)
                    yellow_dict[char] = [count, index_list]
                    continue 
                else:
                    grey_list.append(char)
                    
    # Comparing the guess with the lists and dictionary          
    for i in range(len(guess)):
        char = guess[i]
        for tup in green_list:
            if tup[0] == i:
                if tup[1] == char:
                    continue
                else:
                    return False 
        if char in yellow_dict:
            if i not in yellow_dict[char][1]:
                continue 
            else:
                return False 
        else:
            if char in grey_list:
                return False
            else:
                continue
    return True 
    
#Part 4: Candidate Generation
import random

OPERATORS = "+-*%"
EQUALITY = "="
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"

ENABLE_PLAYTEST = True
DEF_DIFFIC = 10

def create_guess(all_info, difficulty=DEF_DIFFIC):
    '''
    Takes information built up from past guesses that is stored in `all_info`, 
    and uses it as guidance to generate a new guess of length `difficulty`.
    '''
    possible_choices = '0123456789+-%*='
    guess_list = []
    if all_info == []:
        for num in range(difficulty):
            sym = random.choice(possible_choices)
            guess_list.append(sym)
            guess = ''.join(guess_list)
        return guess 
    
    # If the all_info is not an empty list
    for num in range(difficulty):
        guess_list.append(possible_choices)
        
    for row in all_info:
        for index, char, color in row:
            if color == GREEN:
                guess_list[index] = char
            elif color == YELLO or color == GREYY:    
                guess_list[index] = guess_list[index].replace(char, '')
    
    op_count = []  # Containing 2 operators and equality that are green
    for sym in guess_list:
        if len(sym) == 1:
            if sym in OPERATORS or sym == EQUALITY:
                op_count.append(sym) 
    
    if EQUALITY in op_count:
        for idx in range(len(guess_list)):
            if len(guess_list[idx]) == 1:
                continue
            else:
                # Removing all '=' at guess_list if the green equality is found
                if EQUALITY in guess_list[idx]:
                    guess_list[idx] = guess_list[idx].replace(EQUALITY, '')
                else:
                    continue 
                    
    if len(op_count) == 3:
        for num in range(len(guess_list)):
            if len(guess_list[num]) == 1:
                continue
            else:
                for digit in guess_list[num]:
                    # Removing other operators that are not in the op_count
                    if digit in OPERATORS and digit not in op_count:
                        guess_list[num] = guess_list[num].replace(digit, '')

    # Making the random guess                     
    final_list = []
    for nums in guess_list:
        if len(nums) == 1:
            final_list.append(nums)
        else:
            final_list.append(random.choice(nums))
    guess = ''.join(final_list)
    return guess
  