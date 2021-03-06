# coding=utf-8
import csv
import sys
import numpy as np
import math

def calccos(ar1, ar2):
    v1len = 0
    v2len = 0
    ins = 0
    if (len(ar1) == 12): # 一年分
        for i in range(len(ar1)):
            v1len += ar1[i]*ar1[i]
            v2len += ar2[i]*ar2[i]
            ins += ar1[i] * ar2[i]
    else: # 三年分
        for i in range(0, 3):
            for j in range(0, 12):
                v1len += ar1[i][j] * ar1[i][j]
                v2len += ar2[i][j] * ar2[i][j]
                ins += ar1[i][j] * ar2[i][j]
                

    return ins / math.sqrt(v1len) / math.sqrt(v2len)

def calceuclid2(ar1, ar2):
    s = 0
    for i in range(len(ar1)):
        s += (ar1[i]-ar2[i])**2
    return math.sqrt(s)/12

def calceuclid(ar1, ar2):
    s = 0
    for i in range(len(ar1)):
        s += abs(ar1[i]-ar2[i])
    return s/12


# ファイルの読み込み
n_topics = 0
ar = np.zeros((200, 10, 12)) # 200トピック10年分12カ月で仮置き
line = 0

with open(sys.argv[1]) as f:
    reader  = csv.reader(f, delimiter=',')
    for r in reader:
        # 最初の行ではトピック数の決定
        if (n_topics == 0):
            n_topics = len(r) - 1
            print("len={}".format(n_topics))
        else:
#            print(r)
            for t in range(n_topics):
                ar[t][int(line / 12)][line % 12] = float(r[t + 1])
            line = line + 1

# sim = calccos(ar[0], ar[1])

# 同じ話題の年ごとのコサイン類似度
print("cos similarity(same topic)")
for i in range(0, 20):
    sim1 = calccos(ar[i][0], ar[i][1])
    sim2 = calccos(ar[i][1], ar[i][2])
    sim3 = calccos(ar[i][0], ar[i][2])
    print("{},{},{},{}".format(i, sim1, sim2, sim3))

sim = np.zeros((20, 20))
# 最初の年の話題間のコサイン類似度
print("cos similarity between first year's topics")
for i in range(0, 20):
    for j in range(0, 20):
        sim[i][j] = calccos(ar[i][0], ar[j][0])

for i in range(0, 20):
    for j in range(0, 20):
        if j == 19:
            print(sim[i][j])
        else:
            print(sim[i][j], end=",")

# 単位ベクトルとのコサイン類似度
e = np.ones((12))
print("cos similarity vs e")
for i in range(0, 20):
    sim1 = calccos(ar[i][0], e)
    sim2 = calccos(ar[i][1], e)
    sim3 = calccos(ar[i][2], e)
    print("{},{},{},{}".format(i, sim1, sim2, sim3))


# 三年間の話題間のコサイン類似度
for i in range(0, 3):
    print("FY {} cosine similarity between topic".format(i+2015))
    # ヘッダ行
    print("", end=",")
    for j in range(0, 20):
        print(j, end=",")
    print("")
    for j in range(0, 20):
        print(j, end=",")
        for k in range(0, 20):
            if j == k:
                print("-", end=",")
            else:
                print(calccos(ar[j], ar[k]), end=",")
        print("")
            


# 正規化しないユークリッド距離を出してみる
print("before normalyzed euclid distance(^2) between years")
for i in range(0, 20):
    d12 = calceuclid2(ar[i][0], ar[i][1])
    d13 = calceuclid2(ar[i][0], ar[i][2])
    d23 = calceuclid2(ar[i][1], ar[i][2])
    print("{},{},{},{}".format(i, d12, d13, d23))

sim = np.zeros((20, 20))
# 最初の年の話題間のユークリッド距離
print("first topic")
for i in range(0, 20):
    for j in range(0, 20):
        sim[i][j] = calceuclid2(ar[i][0], ar[j][0])

for i in range(0, 20):
    for j in range(0, 20):
        if j == 19:
            print(sim[i][j])
        else:
            print(sim[i][j], end=",")

print("before normalyzed euclid distance between years")
for i in range(0, 20):
    d12 = calceuclid(ar[i][0], ar[i][1])
    d13 = calceuclid(ar[i][0], ar[i][2])
    d23 = calceuclid(ar[i][1], ar[i][2])
    print("{},{},{},{}".format(i, d12, d13, d23))

sim = np.zeros((20, 20))
# 最初の年の話題間のユークリッド距離
print("first topic")
for i in range(0, 20):
    for j in range(0, 20):
        sim[i][j] = calceuclid(ar[i][0], ar[j][0])

for i in range(0, 20):
    for j in range(0, 20):
        if j == 19:
            print(sim[i][j])
        else:
            print(sim[i][j], end=",")

# ユークリッド距離
# 一年目と二年目
# 二年目と三年目
# 標準化処理
for i in range(20):
    for j in range(3):
        s = 0
        s2 = 0
        for k in range(12):
            s += ar[i][j][k]
            s2 += ar[i][j][k]**2
        avg = s/12
        sdev = math.sqrt((s2 - avg**2 * 12) / (12 - 1))
        for k in range(12):
            ar[i][j][k] = (ar[i][j][k] - avg) / sdev



print("normalyzed euclid distance(^2) between years")
for i in range(0, 20):
    d12 = calceuclid2(ar[i][0], ar[i][1])
    d13 = calceuclid2(ar[i][0], ar[i][2])
    d23 = calceuclid2(ar[i][1], ar[i][2])
    print("{},{},{},{}".format(i, d12, d13, d23))

sim = np.zeros((20, 20))
# 最初の年の話題間のユークリッド距離
print("first topic")
for i in range(0, 20):
    for j in range(0, 20):
        sim[i][j] = calceuclid2(ar[i][0], ar[j][0])

for i in range(0, 20):
    for j in range(0, 20):
        if j == 19:
            print(sim[i][j])
        else:
            print(sim[i][j], end=",")

print("normalyzed euclid distance between years")
for i in range(0, 20):
    d12 = calceuclid(ar[i][0], ar[i][1])
    d13 = calceuclid(ar[i][0], ar[i][2])
    d23 = calceuclid(ar[i][1], ar[i][2])
    print("{},{},{},{}".format(i, d12, d13, d23))

sim = np.zeros((20, 20))
# 最初の年の話題間のユークリッド距離
print("first topic")
for i in range(0, 20):
    for j in range(0, 20):
        sim[i][j] = calceuclid(ar[i][0], ar[j][0])

for i in range(0, 20):
    for j in range(0, 20):
        if i == j:
            print("-", end=",")
        elif j == 19:
            print(sim[i][j])
        else:
            print(sim[i][j], end=",")

# 三年間の話題間のユークリッド距離(正規化済み)
for i in range(0, 3):
    print("FY {} normalized euclid distance between topic".format(i+2015))
    # ヘッダ行
    print("", end=",")
    for j in range(0, 20):
        print(j, end=",")
    print("")
    for j in range(0, 20):
        print(j, end=",")
        for k in range(0, 20):
            if j == k:
                print("-", end=",")
            else:
                print(calceuclid(ar[j], ar[k]), end=",")
        print("")