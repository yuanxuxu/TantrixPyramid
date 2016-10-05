# -*- coding: utf-8 -*-

# The solution is based on hints given by teacher during the lab time, 
# which save me lots of trouble implementing the search.py model. 
# The result and goal_test design are really fascinating.
# I modify it to the general form, which should solve all the Trantrix 
# pyramid problem theoretically.
#======================================================================

import math
import search


""" The tiles are arranged in such a way (the pyramid is rotated
        -90 degrees because of ascii convenience):
                           ___
                          /   \
                         /     \
                     ___/   5   \
                    /   \       /
                   /     \     /
               ___/   2   \___/
              /   \       /   \
             /     \     /     \
            /   0   \___/   4   \
            \       /   \       /
             \     /     \     /
              \___/   1   \___/
                  \       /   \
                   \     /     \
                    \___/   3   \
                        \       /
                         \     /
                          \___/
        The numbers of sides in tiles are taken to be
                     _2_
                    /   \
                   1     3
                  /       \
                  \       /
                   0     4
                    \_5_/

        (The tile is also rotated -90 degrees)
    """


# We actually have 15 tiles, thus we call those realTiles.

realTiles=[

    ('b', 'b', 'r', 'r', 'y', 'y'),

    ('y', 'r', 'r', 'b', 'b', 'y'),

    ('g', 'b', 'b', 'y', 'y', 'g'),

    ('b', 'b', 'r', 'y', 'y', 'r'),

    ('b', 'y', 'y', 'b', 'r', 'r'),

    ('b', 'b', 'y', 'g', 'g', 'y'),

    ('g', 'r', 'r', 'g', 'y', 'y'),

    ('r', 'g', 'y', 'r', 'y', 'g'),

    ('r', 'y', 'b', 'y', 'r', 'b'),

    ('g', 'b', 'g', 'r', 'b', 'r'),

    ('y', 'r', 'y', 'b', 'r', 'b'),

    ('b', 'g', 'y', 'y', 'b', 'g'),

    ('g', 'g', 'b', 'y', 'b', 'y'),

    ('y', 'b', 'b', 'r', 'y', 'r'),

    ('r', 'b', 'y', 'y', 'r', 'b')

   ]
   

initialState = [None,None,None,None,None,None,None,None,None,None,None,None,\

               None,None,None]

# consider of speed, we'll use 3 tiles for comparision of performance 

realTiles2=[
   ('y','r','b','b','r','y'),
   ('y','b','r','r','b','y'),
   ('y','r','y','b','b','r')
   ]
   
initialState2 = [None,None,None]


# rotation function

def leftShift(tup, n):

# Taken from http://stackoverflow.com/questions/5299135/how-to-efficiently-
# left-shift-a-tuple

    if not tup or not n:

        return tup

    n %= len(tup)

    return tup[n:] + tup[:n]


# this function return (i,0) for leftmost tiles, (i,i) for right most tiles
# and (-2, -1) for others

def l_r_position_to_row(j):   

    i = (2*j+(1/4))**(1/2)-(1/2)

    if(i.is_integer()):

        return (int(i),0)

    else:

        i = (2*j+(9/4))**(1/2)-(3/2)

        if(i.is_integer()):

            return (int(i),int(i))

    return (-2,-1)


# when it comes from function l_r_position_to_row(j)'s other case, which
# are the middle tiles, get its row

def mid_position_to_row(j): 

    i = (2*j+(1/4))**(1/2)-(1/2)

    return math.floor(i)



class TantrixPyramidN(search.Problem):

    # To generalizer the problem, through observation, we discover the
    # relation between position of tile(a(i)) and its row i:

    # In case of leftmost(ai0):
    # a(i)=(i^2+i)/2, whcih can be written as i=(2*a(i)+(1/4))**(1/2)-(1/2)

    # In case of rightmost(aii):
    # a(i)=(i^2+i)/2 + i, whcih can be written as i=(2*a(i)+(9/4))**(1/2)-(3/2)


    tiles = set()

    
    def __init__(self,initial,realTiles):

        self.initial = tuple(initial) 

        for dummy_tile in realTiles:

            for dummy_i in range(0,6):

                self.tiles.add(leftShift(dummy_tile,dummy_i)) 


    def actions(self,state):

        p =  state.index(None) # give the first None to p

        a = l_r_position_to_row(p)
        
        
        # remove the existing state non-None index to avoid over-used tile
        
        def remove_existing_tile(state):
            
            enabledActions = set(self.tiles)
            
            for dummy_t in state:
                
                if dummy_t is not None:
                
                    for dummy_k in range(0,6):
                
                        enabledActions.remove(leftShift(dummy_t,dummy_k))
            
            return enabledActions
        
    
        # initail case, 0 postion will retrun a=(0,0)

        if a[0] == 0 and a[1] == 0:

            return self.tiles
        
        
        # leftmost case, such as 1,3,6,10... return a=(i,0) 

        elif a[1] == 0:
            
            enabledActions = remove_existing_tile(state)

            # look for the previous leftmost

            previous = state[p-a[0]]  

            # remove the tiles that do not have matching color

            for dummy_t in enabledActions.copy():

                if previous[4]!=dummy_t[1]:

                    enabledActions.remove(dummy_t)
            

        # rightmost case, such as 2, 5, 9, 14... return a=(i,i)

        elif a[1] == a[0]:
            
            enabledActions = remove_existing_tile(state)
    
            # first, look for the previous rightmost

            previous = state[p-a[0]]

            # second, look for left one (position -1)

            left = state[p-1]

            # remove the tiles that do not have matching color

            for dummy_t in enabledActions.copy():

                if previous[3]!=dummy_t[0] or left[2]!=dummy_t[5]: 

                    enabledActions.remove(dummy_t)
        

        # now go on to the midlle tiles, such as 4, 7, 8...

        else:
            
            enabledActions = remove_existing_tile(state)
                    
            # let's get the row of it first

            r = mid_position_to_row(p)

            # cosider its adjaciencies p-1, p-a-1,p-a

            # position p-a-1

            previous_left = state[p-r-1]

            # position p-a

            previous_right = state[p-r]

            # position p-1

            left = state[p-1]

            # remove the tiles that do not have matching color

            for dummy_t in enabledActions.copy():

                if previous_left[3]!=dummy_t[0] or previous_right[4]!=dummy_t[1] or left[2]!=dummy_t[5]: 
                    
                    enabledActions.remove(dummy_t)

        
        return enabledActions
           

    def result(self, state, action):
        
        # Replace the first None with the action.

        newState = list(state)

        p = state.index(None) 

        newState[p] = action
        
        return tuple(newState)


    def goal_test(self, state):

        for el in state:

            if el is None:

                return False

        return True

    
    def h(self, node):
    
        # color 'g' is the fewest, discourage using it
        
        sum = 0
        
        if 'g' in node.state:
            
            sum = sum + 1
        
        return sum
    
tp15 = TantrixPyramidN(initialState,realTiles)
search.depth_first_graph_search(tp15)

# Uncomment the following for compare performance
# result is number of successors/goal tests/ states/ first 4 bytes found

#search.compare_searchers([tp15],["algorithm","Tantrix pyramid 15"],[
#        search.breadth_first_search,
#        search.depth_first_graph_search,
#        search.astar_search
#   ])
