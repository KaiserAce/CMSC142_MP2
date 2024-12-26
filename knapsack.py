import random
from timeit import default_timer as timer
import sys
import numpy as np 

sys.setrecursionlimit(100000000)

recomputed = 0
retrieved = 0

def randomItemGen(n):
    items = []
    for _ in range(n):
        items.append((random.randint(100, 1500), random.randint(100, 500)))
    return items
        
def DPKnapsack(items, WEIGHT=1000):
    V = [[0 for _ in range(WEIGHT+1)] for _ in range(len(items)+1)]
    for i in range(1, len(items)+1):
        for j in range(WEIGHT+1):
            if items[i-1][0] <= j:
                V[i][j] = max(V[i-1][j], items[i-1][1] + V[i-1][j - items[i-1][0]])
            else:
                V[i][j] = V[i-1][j]
    return V[len(items)][WEIGHT], V

def DPMFKnapsack(items, WEIGHT=1000):
    V = [[-1 for _ in range(WEIGHT+1)] for _ in range(len(items)+1)]
    for i in range(WEIGHT+1):
        V[0][i] = 0
    for j in range(len(items)+1):
        V[j][0] = 0
    global recomputed
    global retrieved
    recomputed = 0
    retrieved = 0
    def recurse(i, j):
        global recomputed
        global retrieved
        if V[i][j] < 0:
            if j < items[i-1][0]:
                value = recurse(i-1, j)
            else:
                value = max(recurse(i-1, j), items[i-1][1] + recurse(i-1, j - items[i-1][0]))
            V[i][j] = value
            recomputed += 1
        else:
            retrieved += 1
        return V[i][j]
    recurse(len(items), WEIGHT)
    return V[len(items)][WEIGHT], V, recomputed, retrieved

def DPKnapsackBacktracking(items, DP, WEIGHT=1000):
    included = []
    for i in range(len(items), 0, -1):
        if DP[i][WEIGHT] != DP[i - 1][WEIGHT]:
            included.append(items[i - 1])
            WEIGHT -= items[i - 1][0]
    included.reverse()
    return included

def LVGreedyKnapsack(items, WEIGHT=1000):
    arr = items.copy()
    arr.sort(key=lambda tup: tup[1], reverse=True)
    total_value = 0
    included = []
    while arr and WEIGHT != 0:
        if arr[0][0] <= WEIGHT:
            WEIGHT -= arr[0][0]
            total_value += arr[0][1]
            included.append((arr[0], arr[1]))
            arr.pop(0)
        else:
            arr.pop(0)
    return total_value, included

def SWGreedyKnapsack(items, WEIGHT = 1000):
    arr = items.copy()
    arr.sort(key=lambda tup: tup[0])
    total_value = 0
    included = []
    while arr and WEIGHT != 0:
        if arr[0][0] <= WEIGHT:
            WEIGHT -= arr[0][0]
            total_value += arr[0][1]
            included.append((arr[0], arr[1]))
            arr.pop(0)
        else:
            arr.pop(0)
    return total_value, included
    
def VRGreedyKnapsack(items, WEIGHT=1000):
    ratio = []
    for item in items:
        temp = item + (item[1]/item[0],)
        ratio.append(temp)
    ratio.sort(key=lambda tup: tup[2], reverse=True)
    value = 0
    included = []
    while ratio and WEIGHT != 0:
        if ratio[0][0] <= WEIGHT:
            value = value + ratio[0][1]
            WEIGHT = WEIGHT - ratio[0][0]
            included.append((ratio[0][0], ratio[0][1]))
            ratio.pop(0)
        else:
            ratio.pop(0)
    return value, included

def validityChecker():
    items1 = [(2, 12), (1, 10), (3, 20), (2, 15)]
    print(DPKnapsack(items1, 5))
    print(DPMFKnapsack(items1, 5))
    DP = DPKnapsack(items1, 5)[1]
    print(DPKnapsackBacktracking(items1, DP, 5))
    print(LVGreedyKnapsack(items1,5))
    print(SWGreedyKnapsack(items1,5))
    print(VRGreedyKnapsack(items1, 5))
    
def algo_runtime(algorithm, items):
    start = timer()
    result = algorithm(items)
    end = timer()
    return(end-start)* 10**3, result[0], result[1]

def experimentParameters():
    i = 100
    data = []
    while i <= 100000:
        items = randomItemGen(i)
        
        time = []
        for _ in range(3):
            start = timer()
            result = DPKnapsack(items)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'DPKnapsack', result[0], time[0], time[1], time[2], np.average(time)))
        DP = result[1]

        time = []
        for _ in range(3):
            start = timer()
            result = DPMFKnapsack(items)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'DPMFKnapsack', result[0], time[0], time[1], time[2], np.average(time), result[2], result[3]))

        time = []
        for _ in range(3):
            start = timer()
            result = DPKnapsackBacktracking(items, DP)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'DPKnapsackBacktracking', 'N/A', time[0], time[1], time[2], np.average(time), result[0]))

        time = []
        for _ in range(3):
            start = timer()
            result = LVGreedyKnapsack(items)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'LargestValueKnapsack', result[0], time[0], time[1], time[2], np.average(time), result[1]))

        time = []
        for _ in range(3):
            start = timer()
            result = SWGreedyKnapsack(items)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'SmallestWeightKnapsack', result[0], time[0], time[1], time[2], np.average(time), result[1]))

        time = []
        for _ in range(3):
            start = timer()
            result = VRGreedyKnapsack(items)
            end = timer()
            time.append((end-start) * 10**3)
        data.append((i, 'ValueRatioKnapsack', result[0], time[0], time[1], time[2], np.average(time), result[1]))

        if i < 1000:
            i += 100
        elif i < 10000:
            i += 1000
        elif i <= 100000:
            i += 10000

    print("Bottom-up and Memoized Dynamic Programming Knapsack")
    print(f"{'i':<10}{'Bottom-up (ms)':<30}{'Memoized (ms)':<30}")
    data1 = []
    data2 = []
    for i in data:
        if i[1] == 'DPKnapsack':
            data1.append((i[0], i[6]))

        elif i[1] == 'DPMFKnapsack':
            data2.append((i[0], i[6]))
    while data1:
        print(f"{data1[0][0]:<10}{data1[0][1]:<30}{data2[0][1]:<30}")
        data1.pop(0)
        data2.pop(0)

    print()

    print("Recomputations and Retrievals of Memoized Dynamic Programming")
    print(f"{'i':<10}{'Recomputations':<20}{'Retrievals':<20}")
    for i in data:
        if i[1] == 'DPMFKnapsack':
            print(f"{i[0]:<10}{i[7]:<20}{i[8]:<20}")

    print()

    print("Time Efficiency of Backtracking Algorithm for Dynamic Programming Knapsack")
    print(f"{'i':<10}{'Trial 1 (ms)':<30}{'Trial 2 (ms)':<30}{'Trial 3 (ms)':<30}{'Ave. Runtime (ms)':<30}")
    for i in data:
        if i[1] == 'DPKnapsackBacktracking':
            print(f"{i[0]:<10}{i[3]:<30}{i[4]:<30}{i[5]:<30}{i[6]:<30}")

    print()
    print("Computed Values of Greedy Algorithms for Knapsack Problem")
    print(f"{'':<10}{'':<20}{'Largest Value First':<50}{'Smallest Weight First':<50}{'Greatest Value-Ratio First':<50}")
    print(f"{'i':<10}{'Actual Max Value':<20}{'Computed Value':<15}{'Absolute Error':<15}{'Relative Err. (%)':<20}{'Computed Value':<15}{'Absolute Error':<15}{'Relative Err. (%)':<20}{'Computed Value':<15}{'Absolute Error':<15}{'Relative Err. (%)':<20}")
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    for i in data:
        if i[1] == 'DPKnapsack':
            data1.append((i[0], i[2]))
        elif i[1] == 'LargestValueKnapsack':
            data2.append(i[2])
        elif i[1] == 'SmallestWeightKnapsack':
            data3.append(i[2])
        elif i[1] == 'ValueRatioKnapsack':
            data4.append(i[2])
    while data1:
        print(f"{data1[0][0]:<10}{data1[0][1]:<20}{data2[0]:<15}{(data1[0][1]-data2[0]):<15}{((data1[0][1]-data2[0])/data1[0][1])*100:<20.5f}{data3[0]:<15}{(data1[0][1]-data3[0]):<15}{((data1[0][1]-data3[0])/data1[0][1])*100:<20.5f}{data4[0]:<15}{(data1[0][1]-data4[0]):<15}{((data1[0][1]-data4[0])/data1[0][1])*100:<20.5f}")
        data1.pop(0)
        data2.pop(0)
        data3.pop(0)
        data4.pop(0)

    print()

    print("Average runtimes of Algorithms (ms)")
    print(f"{'i':<10}{'DPKnapsack':<30}{'DPMFKnapsack':<30}{'DPKnapsackBacktracking':<30}{'DPKnapsack + Backtracking':<30}{'DPMFKnapsack + Backtracking':<30}{'LVGreedyKnapsack':<30}{'SWGreedyKnapsack':<30}{'VRGreedyKnapsack':30}")
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for i in data:
        if i[1] == 'DPKnapsack':
            data1.append((i[0], i[6]))
        elif i[1] == 'DPMFKnapsack':
            data2.append(i[6])
        elif i[1] == 'DPKnapsackBacktracking':
            data3.append(i[6])
        elif i[1] == 'LargestValueKnapsack':
            data4.append(i[6])
        elif i[1] == 'SmallestWeightKnapsack':
            data5.append(i[6])
        elif i[1] == 'ValueRatioKnapsack':
            data6.append(i[6])
    while data1:
        print(f"{data1[0][0]:<10}{data1[0][1]:<30}{data2[0]:<30}{data3[0]:<30}{data1[0][1]+data3[0]:<30}{data2[0]+data3[0]:<30}{data4[0]:<30}{data5[0]:<30}{data6[0]:<30}")
        data1.pop(0)
        data2.pop(0)
        data3.pop(0)
        data4.pop(0)
        data5.pop(0)
        data6.pop(0)

    print()

    print("Raw Data")
    for i in data:
        if i[1] == 'DPKnapsack':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}")
        elif i[1] == 'DPMFKnapsack':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}; Recomputation: {i[7]}; Retrievals: {i[8]}")
        elif i[1] == 'DPKnapsackBacktracking':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}")
            print(f"Solution: {i[7]}")
        elif i[1] == 'LargestValueKnapsack':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}")
            print(f"Solution: {i[7]}")
        elif i[1] == 'SmallestWeightKnapsack':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}")
            print(f"Solution: {i[7]}")
        elif i[1] == 'ValueRatioKnapsack':
            print(f"i = {i[0]}; {i[1]}; Computed Value: {i[2]}; Trial 1: {i[3]}; Trial 2: {i[4]}; Trial 3: {i[5]}; Ave. Runtime: {i[6]}")
            print(f"Solution: {i[7]}")
        
# validityChecker()
experimentParameters()
