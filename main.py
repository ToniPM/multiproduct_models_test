from xp import xp
from itertools import product

from ProductMove import ProductMove
from States import ForgetfulState, OvercomplicatedState

if __name__ == '__main__':

    def flatten(l):
        return sum([flatten(item) if hasattr(item, "__iter__") else [item] for item in l], [])

    def valid_matrices(qt_vars, qt_targets):
        for f in product((0, 1), repeat=qt_vars*qt_targets):
            target_matrix = xp.reshape(xp.asarray(f), (qt_vars, qt_targets))
            if xp.all(xp.any(target_matrix, axis=0)) and xp.all(xp.any(target_matrix, axis=1)):
                yield target_matrix


    for matrix in valid_matrices(4, 4):
        state = OvercomplicatedState.from_target_matrix(matrix)
        i = 0
        states = [(state,[])]
        if state.is_finished():
            solving_moves = []
        else:
            break_flag = False
            while states:
                state, moves = states.pop(0)
                i+=1
                if i%100==0:
                    print(i)
                for move in state.available_moves():
                    new_state = state.move(move)
                    if new_state.is_finished():
                        final_state = new_state
                        solving_moves = (moves,move)
                        break_flag = True
                        break
                    states.append((new_state,(moves,move)))
                if break_flag: break
        solving_moves_x = flatten(solving_moves)

        state = ForgetfulState.from_target_matrix(matrix)
        i = 0
        states = [(state,[])]
        if state.is_finished():
            solving_moves = []
        else:
            break_flag = False
            while states:
                state, moves = states.pop(0)
                i+=1
                if i%100==0:
                    print(i)
                for move in state.available_moves():
                    new_state = state.move(move)
                    if new_state.is_finished():
                        final_state = new_state
                        solving_moves = (moves,move)
                        break_flag = True
                        break
                    states.append((new_state,(moves,move)))
                if break_flag: break
        solving_moves_t = flatten(solving_moves)


        print(matrix,"\n",solving_moves_x,"\n",solving_moves_t,"\n"*3)
        if len(solving_moves_x)!=len(solving_moves_t):
            print("ojo al manojo!")
            input()
        #state = OvercomplicatedState.from_target_matrix(matrix)
        #for move in flatten(solving_moves):
        #    state = state.move(move)
        #    print(move,"\n",state.known)
        #print("\n"*3)
        #input()

    print(jjsj)

    state = OvercomplicatedState.from_targets(((0,1),(1,2),(1,2,0)))
    #state = OvercomplicatedState.from_targets(((0,1),(1,2)))
    #state = ForgetfulState.from_targets(((0,1),(1,2),(2,3),(1,2,3,0)))
    #state = ForgetfulState.from_target_matrix(xp.random.rand(5,5)>0.5)
    #print(state.targets)

    states = [(state,[])]

    #won't catch if starting state is finished
    print(state.targets)
    input()
    i = 0
    while states:
        state, moves = states.pop(0)
        i+=1
        if i%100==0:
            print(i)
        for move in state.available_moves():
            new_state = state.move(move)
            if new_state.is_finished():
                final_state = new_state
                solving_moves = (moves,move)
            states.append((new_state,(moves,move)))
    print(flatten(solving_moves))