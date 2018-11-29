#############################
# MUTLITHREADING TEST PROGRAM
#############################

from multiprocessing import Process, Queue
import pandas as pd
import random as rd
import numpy as np
# import matplotlib as mp
# from simple_benchmark import benchmark


def simulation(dat, q):

    dat.loc[i] = [round(rd.random()) for n in range(3)]
    # dat.append([round(rd.random())])
    q.put(dat)


def save(q):

    dat = q.get()
    testcsv = dat.to_csv('/home/timothe/WORK/community_ecology/python-code/test1.csv', mode='a', header=False)
    testcsv


q = Queue()
# INITIALIZING THE CSV FILE
data = pd.DataFrame(columns=['CC1', 'CC2', 'CC3'])
testcsv = data.to_csv('/home/timothe/WORK/community_ecology/python-code/test1.csv', header=True)
testcsv
procs =[]

for i in range(100):
    proc1 = Process(target=simulation, args=(data, q))
    proc2 = Process(target=save, args=(q, ))
    procs.append(proc1)
    procs.append(proc2)
    proc1.start()
    proc2.start()

for proc in procs:
    q.close()
    q.join_thread()
    proc1.join()
    proc2.join()



# BENCHMARK ESTIMATION

# funcs = [std_csv(), parallel_csv()]
# aliases = {std_csv: 'Standard for loop', parallel_csv: 'Parallel Processing'}
# b = benchmark(funcs, function_aliases=aliases)

# b.plot()


