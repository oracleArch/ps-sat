import subprocess as sp
import argparse
import os
import re

csat = os.environ['CSAT']
kissat = os.environ['KISSAT']
pssat = os.environ['PSSAT']

# Add argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--vars',help='N values for desired CNF formulae', type=int, nargs='+', required=True)
parser.add_argument('--alpha', help='Ratio of clauses to variables', type=float, required=True)
parser.add_argument('--betav', help='Variable beta', type=float, required=True)
parser.add_argument('--betac', help='Clause beta', type=float, default=0.0)
parser.add_argument('--temp', help='Temperature to determine formula entropy', type=float, required=True)
parser.add_argument('--seed', help='Random seed', type=int, default=0)
parser.add_argument('--inst', help='Number of problems to generate', type=int, default=20)
parser.add_argument('--outformat', help='Format string for n, m, betav, betac, temp respectively', default='cust-ps{}-{}_bv{}_bc{}_t{}')
parser.add_argument('--out', help='Output parent directory', default=csat)

parser.add_argument('--reorder', help='Whether to rename vars/reorder clauses based on similarity', action='store_true', default=False)


# run a single instance of ps-sat and return the output
def run_pssat(n: int, m: int, betav: float, betac: float, temp: float, seed:int, reorder:bool)->str:
    output = sp.run([pssat, 
                     f'-n {n}',
                     f'-m {m}',
                      '-k 0',
                      '-K 3',
                     f'-b {betav}',
                     f'-B {betac}',
                     f'-T {temp}',
                      '' if not reorder else '-r',
                     f'-s {seed}'], stdout=sp.PIPE)
    stdout_str = output.stdout.decode('utf-8')
    return stdout_str

# write generated to CNF output
def write_cnf(output_dir: str, problem_dir: str, problem_inst: str, cnfstr: str):
    output_path = os.path.join(output_dir, problem_dir)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, problem_inst), mode='w') as outfile:
        outfile.write(cnfstr)

if __name__ == '__main__':
    args = parser.parse_args()
    for n in args.vars: 
        m = round(n * args.alpha)
        print(f'N: {n}, M: {m}')
        output_vars = [n,m, args.betav, args.betac, args.temp]
        problem_dir = args.outformat.format(*output_vars)
        for i in range(args.inst):
            output_inst = 'cust-ps{}-0{}.cnf'.format(n, i)
            cnf = run_pssat(n, m, args.betav, args.betac, args.temp, args.seed, args.reorder)
            write_cnf(args.out, problem_dir, output_inst, cnf)



