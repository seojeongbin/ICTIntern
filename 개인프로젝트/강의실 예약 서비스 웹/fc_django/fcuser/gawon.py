import numpy as np

randgen = np.random.RandomState(1)
w = randgen.normal(loc=0.0, scale=0.01, size=3)

for i in w:
    print(i)
