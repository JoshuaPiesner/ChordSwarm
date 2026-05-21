import numpy as np
import random
import datetime as dt

# Loss Functions / Reward Functions

# Circle of fifths distance
'''
    Assumes 0<=n<=12
'''
def circ_dist(n: int) -> int:
    if (n%2)==0: return min(n, abs(n-12))
    else: return abs(min(n, abs(n-12))-6)

'''
  - X : X (4,n)
  - C : List of chords in their mod12 values (m,n)
'''
def chord_similarity(X: np.ndarray, C: np.ndarray):
    # Take min circle of fifths distance from chord for each note
    n = X.shape[1]
    m = C.shape[0]
    X = np.repeat(X.T.flatten(), m, axis=0)
    C = np.repeat(C, 4, axis=1)
    Y = X-C
    Y = Y %12
    circ_distv = np.vectorize(circ_dist)
    Y = circ_distv(Y)
    score = np.min(Y, axis=0)
    score = np.matrix(score)
    score = score.reshape((n,4))
    return score.T * -1

'''
    Assumes X.shape = (4,n)
'''
def get_distances(X: np.ndarray) -> np.ndarray:
    DIST_MATRIX = np.matrix([
        [1,-1,0,0],
        [1,0,-1,0],
        [1,0,0,-1],
        [0,1,-1,0],
        [0,1,0,-1],
        [0,0,1,-1]
    ])
    return DIST_MATRIX * X


def interval_dist(x: int) -> int:
    return 12 if (x != 0 and x%12==0) else x%12
interval_distv = np.vectorize(interval_dist)

'''
    Assumes X.shape = (4,n)
'''
def get_interval_distances(X: np.ndarray) -> np.ndarray:
    return interval_distv(get_distances(X))  #(6,n) matrix

'''
    Assumes X.shape = (4,n)
'''
def parallel_octaves(X: np.ndarray) -> np.ndarray:
    n = X.shape[1]
    DISTS = get_interval_distances(X) #(6,n) matrix
    is12 = np.vectorize(lambda x : 1 if x==12 else 0)
    DISTS = is12(DISTS)
    array = []
    for i in range(n-1):
        row = [0]*n
        row[i] = 1
        row[i+1] = 1
        array.append(row)
    MOVES = np.array(array).T
    return np.vectorize(lambda x : 1 if x==2 else 0)(DISTS * MOVES) * -1

'''
    Assumes X.shape = (4,n)
'''
def parallel_fifths(X: np.ndarray) -> np.ndarray:
    n = X.shape[1]
    DISTS = get_interval_distances(X) #(6,n) matrix
    is7 = np.vectorize(lambda x : 1 if x==7 else 0)
    DISTS = is7(DISTS)
    array = []
    for i in range(n-1):
        row = [0]*n
        row[i] = 1
        row[i+1] = 1
        array.append(row)
    MOVES = np.array(array).T
    return np.vectorize(lambda x : 1 if x==2 else 0)(DISTS * MOVES) * -1

    
'''
    Takes in output from parallel_octaves or parallel_fifths: (6,n-1) matrix
    Returns (4,n) matrix
'''
def moves_to_indiv(MOVES: np.ndarray) -> np.ndarray:
    MOVESL = np.hstack((MOVES, ([[0]]*6)))
    MOVESR = np.hstack(([[0]]*6, MOVES))
    MOVES = MOVESL + MOVESR
    SUM_MATRIX = np.matrix([
        [1,1,1,0,0,0], #represents how we differenced in get_distances
        [1,0,0,1,1,0],
        [0,1,0,1,0,1],
        [0,0,1,0,1,1]
    ])
    return (SUM_MATRIX *MOVES)

'''
    Assumes X.shape = (4,n)
    Penalizes if higher voice is lower than lower voice
'''
def crossings(X: np.ndarray) -> np.ndarray:
    DISTS = get_distances(X)
    DISTS = np.vectorize(lambda x : 1 if x > 0 else 10*x)(DISTS)
    SUM_MATRIX = np.matrix([
        [1,1,1,0,0,0], #represents how we differenced in get_distances
        [1,0,0,1,1,0],
        [0,1,0,1,0,1],
        [0,0,1,0,1,1]
    ])
    RESULT = (SUM_MATRIX *DISTS)
    return RESULT - np.full(RESULT.shape, 3)

'''
    Assumes X.shape = (4,n)
'''
def crossing_info(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    DISTS = get_distances(X)
    DISTS = np.vectorize(lambda x : 0 if x > 0 else (x-1))(DISTS)
    ARR1 = []
    ARR2 = []
    ARR3 = []
    ARR1.append(DISTS[0, :] * (-1))
    ARR1.append(DISTS[0, :])
    ARR1.append(DISTS[1, :])
    ARR1.append(DISTS[2, :])
    ARR2.append(DISTS[1, :]*(-1))
    ARR2.append(DISTS[3, :]*(-1))
    ARR2.append(DISTS[3, :])
    ARR2.append(DISTS[4, :])
    ARR3.append(DISTS[2, :]*(-1))
    ARR3.append(DISTS[4, :]*(-1))
    ARR3.append(DISTS[5, :]*(-1))
    ARR3.append(DISTS[5, :])
    return np.vstack(ARR1), np.vstack(ARR2), np.vstack(ARR3)


'''
    Assumes X.shape = (4,n)
'''
def continuity(X: np.ndarray) -> np.ndarray:
    n = X.shape[1]
    array = []
    for i in range(n-1):
        row = [0]*n
        row[i] = 1
        row[i+1] = -1
        array.append(row)
    MOVES = np.array(array).T
    MOVES = X * MOVES
    return MOVES
'''
    Assumes X.shape = (4,n)
'''
def continuityR(X: np.ndarray) -> np.ndarray:
    MOVES = continuity(X)
    return np.hstack((MOVES, ([[0]]*4))) * -1
'''
    Assumes X.shape = (4,n)
'''
def continuityL(X: np.ndarray) -> np.ndarray:
    MOVES = continuity(X)
    return np.hstack(([[0]]*4, MOVES))


'''
    Assumes X.shape = (4,n)
'''
def update(X: np.ndarray, C: np.ndarray, 
           chord_sim_strength = 1,
           par_oct_strength = 4000,
           par_fif_strength = 4000,
           cross_info_strength = 40,
           continu_strength = 0.1
           ) -> np.ndarray:
    # before = dt.datetime.now()
    CHORD_SIM = chord_similarity(X,C) # vals from 0 to -6
    PAR_OCT = moves_to_indiv(parallel_octaves(X)) # vals from 0 to 1
    PAR_FIF = moves_to_indiv(parallel_fifths(X)) # vals from 0 to 1
    CROSS_INFO = crossing_info(X) # 0 (if no need to move) otherwise -88 to 88
    CONTINUR = continuityR(X) # -88 to 88 (direction of right in relation to node)
    CONTINUL = continuityL(X) # -88 to 88 (direction of left in relation to node)
    # for each index in X
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            curr_pos = X[i,j]
            usd = [0, 45, 0] #up/stay/down
            # Let chord sim affect probabilities
            usd[0] += (CHORD_SIM[i,j]**12) * chord_sim_strength
            usd[2] += (CHORD_SIM[i,j]**12) * chord_sim_strength
            # Let par_oct affect probabilities
            usd[0] += abs(PAR_OCT[i,j]) * par_oct_strength
            usd[2] += abs(PAR_OCT[i,j]) * par_oct_strength
            # Let par_fif affect probabilities
            usd[0] += abs(PAR_FIF[i,j]) * par_fif_strength
            usd[2] += abs(PAR_FIF[i,j]) * par_fif_strength
            # Let crossing info affect probabilites
            for CROSS_INFOI in CROSS_INFO:
                cross = CROSS_INFOI[i,j]
                if (cross > 0):
                    usd[0] += cross * cross_info_strength
                elif (cross < 0):
                    usd[2] += abs(cross * cross_info_strength)
            # Let continuity affect probabilities
            right = CONTINUR[i,j]
            left = CONTINUL[i,j]
            if (right > 0):
                usd[0] += right * continu_strength
            elif (right < 0):
                usd[2] += abs(right * continu_strength)
            if (left > 0):
                usd[0] += left * continu_strength
            elif (left < 0):
                usd[2] += abs(left * continu_strength)
            # Go up/stay/down based on usd probability
            # if abs(CHORD_SIM[i,j]) > 2:
                # print(CHORD_SIM[i,j], usd)
            total = 0
            for num in usd:
                total += num
            prob = random.random() * total
            run_sum = 0
            for dir in range(len(usd)):
                run_sum += usd[dir]
                # print(usd, end="")
                if (run_sum >= prob):
                    # print(dir)
                    X[i,j] += (1-dir) # If 0: +1, if 1, +0, if 2: -1
                    if (X[i,j] > 88):
                        X[i,j] = 88
                    if (X[i,j] < 36):
                        X[i,j] = 36
                    break
    # after = dt.datetime.now()
    # print((after-before))
    return X, CHORD_SIM.sum(), abs(CONTINUR).sum()*-1