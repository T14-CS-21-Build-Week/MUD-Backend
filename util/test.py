import random

direction = [-1, 1]  # -1 = south or west, 1 = north or east
vertical_or_horizontal = ['x', 'y']

def whoknows():
    one_or_negative_one = random.choice(direction)
    x_or_y = random.choice(vertical_or_horizontal)

    if x_or_y == 'x':    #we are moving east or west
        if one_or_negative_one == 1: #moving east
            print('east')
            #Check if a movement east is within the boundary
        else:  #moving west
            print('west')

    elif x_or_y == 'y':  #we are moving north or south
        # print('north or south')
        if one_or_negative_one == 1: #moving north
            print('north')
        else: 
            print('south')


whoknows()
whoknows()
whoknows()