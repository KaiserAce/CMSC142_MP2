import random
import sys

sys.setrecursionlimit(100000000)

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
    return V[len(items)][WEIGHT]

def DPMFKnapsack(items, WEIGHT=1000):
    V = [[-1 for _ in range(WEIGHT+1)] for _ in range(len(items)+1)]
    for i in range(WEIGHT+1):
        V[0][i] = 0
    for j in range(len(items)+1):
        V[j][0] = 0
    def recurse(i, j):
        if V[i][j] < 0:
            if j < items[i-1][0]:
                value = recurse(i-1, j)
            else:
                value = max(recurse(i-1, j), items[i-1][1] + recurse(i-1, j - items[i-1][0]))
            V[i][j] = value
        return V[i][j]
    recurse(len(items), WEIGHT)
    return V[len(items)][WEIGHT]

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
    return value


def validityChecker():
    items1 = [(2, 12), (1, 10), (3, 20), (2, 15)]
    print(DPKnapsack(items1, 5))
    print(DPMFKnapsack(items1, 5))
    print(VRGreedyKnapsack(items1, 5))

def experimentParameters():
    i = 100
    while i <= 100000:
        items = randomItemGen(i)
        print(DPKnapsack(items))
        print(DPMFKnapsack(items))
        print(VRGreedyKnapsack(items))
        i = i * 10

validityChecker()
experimentParameters()
