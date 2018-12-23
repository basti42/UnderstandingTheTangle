# -*- coding: utf-8 -*-

from numpy import random
import numpy as np
from string import ascii_uppercase
import time
import matplotlib.pyplot  as plt

from TangleNode import Transaction, TangleNode
from Tangle import Tangle


tangle = Tangle()
abc = list(ascii_uppercase)

# tracking
x, validated, nonvalidated = [], [], []

number = 25000
print("Making a Tangle with {} nodes".format(number))
for i in range(number):

    x.append(i)
    validated.append(len(tangle.validatedNodes))
    nonvalidated.append(len(tangle.nodes))
    # if i % 30 == 0: print(tangle)

    f = random.choice(abc)
    t = random.choice(abc)
    a = random.random()

    trans = Transaction(t,f,a)
    tangle.addNode(trans)

print("Tangle with {} nodes created!".format(number))

fig = plt.figure(figsize=(14,10))

plt.subplot(1,2,1)
plt.plot(x, nonvalidated, '-', color="orange", label="non-validated nodes")
plt.plot(x, validated, '-', color="dodgerblue", label="validated nodes")
plt.grid()
plt.legend()
plt.xlabel("total number of nodes")
plt.ylabel("portion validated/non-validated")

plt.subplot(1,2,2)
plt.plot(x, np.array(validated)/np.array(nonvalidated), '-', color="dodgerblue")
plt.grid()
plt.xlabel("total number of nodes")
plt.ylabel("validated / non-validated")
plt.show()
