# -*- coding: utf-8 -*-
"""
Some hints how to solve HW1 in ITI8600.

This is not a complete solution, but gives you an initial
idea how to proceed. Currently can place 3 tiles in a valid way
on the pyramid containing of 6 tiles.

"""

import search

"""
   We actually have 6 tiles, thus we call those realTiles.
   In the instantiation of the Problem class we create all rotations.
"""
realTiles=[
   ('y','r','b','b','r','y'),
   ('y','b','r','r','b','y'),
   ('y','r','y','b','b','r'),
   ('y','b','y','r','b','r'),
   ('y','r','b','r','b','y'),
   ('y','r','y','b','r','b')
   ]

initialState = [None,None,None,None,None,None]

# The data structure is currently not used.
adjacencies = {0:[1,2],
               1:[0,2,3,4],
               2:[0,1,4,5],
               3:[1,4],
               4:[1,2,3,5],
               5:[2,4]}

def leftShift(tup, n):
    """
       Taken from http://stackoverflow.com/questions/5299135/how-to-efficiently-left-shift-a-tuple
    """
    if not tup or not n:
        return tup
    n %= len(tup)
    return tup[n:] + tup[:n]

class TantrixPyramid6(search.Problem):
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
    tiles = set()

    def __init__(self,initial,realTiles):
        self.initial = tuple(initial)
        for tile in realTiles:
            for i in range(0,6):
                self.tiles.add(leftShift(tile,i))

    def actions(self,state):
        """Not complete  yet"""
        i =  state.index(None)
        enabledActions=set(self.tiles)
        if i == 0:
            return enabledActions
        else:
            for j in range(i):
                for k in range(0,6):
                   enabledActions.remove(leftShift(state[j],k))
        if i == 1:
            # get the 0-th tile
            t0 = state[0]
            # remove the tiles that do not have matching color
            toRemove=[]
            for t in enabledActions:
                if t0[4]!=t[1]: # side 4 of the 0th tile is next to
                                # tile 1 of the 1st tile
                    toRemove.append(t)
            for t in toRemove:
                enabledActions.remove(t)
        elif i == 2:
            # get the 0-th tile
            t0 = state[0]
            # get the 1-st tile
            t1 = state[1]
            # remove the tiles that do not have matching color
            toRemove=[]
            for t in enabledActions:
                if t0[3]!=t[0]: # side 4 of the 0th tile is next to
                                # tile 1 of the 1st tile
                    toRemove.append(t)
                elif t1[2]!=t[5]:
                    toRemove.append(t)
            for t in toRemove:
                enabledActions.remove(t)
        # more cases for i = 3 etc.
        # Think if our adjacency data structure is sufficient?
        # may be you need to change it to make the current
        # function more elegant?
        # TODO! (for the 6 tile problem)
        #elif i == 3:
        #elif i == 4:
        #elif i == 5:

        return enabledActions


    def result(self, state, action):
        """ Replace the first None with the action."""
        newState = list(state)
        i = state.index(None)
        newState[i] = action
        return tuple(newState)

    def goal_test(self, state):
        for el in state:
            if el is None:
                return False
        return True

tp6 = TantrixPyramid6(initialState,realTiles)

search.depth_first_graph_search(tp6)

search.breadth_first_search(tp6)

"""
   There are tools available to compare
   search algorithms. The stats contain the following data:
   number of successors /
   number of goal tests /
   number of states /
   first 4 bytes of the found goal
"""
search.compare_searchers([tp6],["algorithm","Tantrix pyramid 6"],[
        search.breadth_first_search,
        search.depth_first_graph_search
    ])
