import os
from subprocess import Popen, PIPE, STDOUT
kissat = os.environ['KISSAT']
pssat = os.environ['PSSAT']
csat = os.environ['CSAT']
from scripts.create_cnf import run_pssat 
import numpy as np
import argparse

bv = 0.5
n = 500
a_arr = np.arange(2, 5, 0.1)
t_arr = np.arange(0.1, 3, 0.1)
results = np.zeros((a_arr.size, t_arr.size))
iters = 20
for (i, alpha) in enumerate(a_arr):
    m = round(alpha * n) 
    for (j, temp) in  enumerate(t_arr):
        counter = 0
        for k in range(iters):
            cnfstr = run_pssat(betac=0, betav=bv, m=m, n=n, reorder=False, seed=k, temp=temp)
            p = Popen([kissat], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            result = p.communicate(input=cnfstr.encode())
            counter += 1 if 's SATISFIABLE' in result[0].decode('utf-8') else 0
        results[i][j] = counter / iters
        if counter == iters:
            break
if not os.path.exists(f'TRANSITIONS/n{n}_bv{bv}'):
    os.makedirs(f'TRANSITIONS/n{n}_bv{bv}')
np.savetxt(X=results, fname=f'TRANSITIONS/n{n}_bv{bv}/a{a_arr[0]}-{a_arr[-1]}_t{t_arr[0]}-{t_arr[-1]}_results.npy')
np.savetxt(X=a_arr, fname=f'TRANSITIONS/n{n}_bv{bv}/a{a_arr[0]}-{a_arr[-1]}_t{t_arr[0]}-{t_arr[-1]}_a_arr.npy')
np.savetxt(X=t_arr, fname=f'TRANSITIONS/n{n}_bv{bv}/a{a_arr[0]}-{a_arr[-1]}_t{t_arr[0]}-{t_arr[-1]}_t_arr.npy')