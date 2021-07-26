from xp import xp
from itertools import product

from ProductMove import ProductMove
from States import ForgetfulState, OvercomplicatedState

if __name__ == '__main__':

    def flatten(l):
        return sum([flatten(item) if hasattr(item, "__iter__") else [item] for item in l], [])

    state = ForgetfulState.from_targets(((0,1),(1,2),(2,3),(3,4),(4,0),(0,1,2,3),(1,2,3,4),(2,3,4,0),(3,4,0,1),(4,0,1,2)))

    states = [(state,[],0)]

    # print(state.targets)
    # input()
    i = 0
    break_flag = False
    while states:
        state, moves, depth = states.pop(0)
        i+=1
        if i%100==0:
            print(i, depth)
        new_depth = depth+1
        for move in state.available_moves():
            new_state = state.move(move)
            if new_state.is_finished():
                final_state = new_state
                solving_moves = (moves,move)
                break_flag = True
                break
            if new_state.qt_finished()==new_depth:
                states.append((new_state,(moves,move), new_depth))
        if break_flag: break
    print(flatten(solving_moves))