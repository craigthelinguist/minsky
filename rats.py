

import sys
from functools import reduce
from operator import mul

def is_prime(p):
    if p == 2: return True
    if p < 2: return False
    if p % 2 == 0: return False
    for i in range(3, p, 2):
        if p % i == 0: return False
    return True

def generate_primes(n):
    x = 2
    primes = []
    while len(primes) < n:
        if is_prime(x): primes.append(x)
        if x == 2: x = 3
        else: x += 2
    return primes

def to_rationals(arity, vectors):
    '''
    Convert the vector game into the corresponding rational game
    :param arity: number of components in each vector.
    :param vector: an iterable sequence of vectors.
    :return: a rational number.
    '''
    primes = generate_primes(arity)
    toRat = lambda v : reduce(mul, [primes[i] ** x for i, x in enumerate(v)])
    return [toRat(v) for v in vectors]

def read_vectors(fname):
    with open(fname, "r") as f:
        line = f.readline().split()
        arity = int(line[0])
        vectors = [ [int(i) for i in line.split()] for line in f ]
        return arity, vectors

def output(arity, vectors, rationals, fpath):
    with open(fpath, "w") as f:
        primes = generate_primes(arity)
        for i, v in enumerate(vectors):
            f.write("Rational " +  str(i) + ":   ")
            for j in range(arity):
                f.write( str(primes[j]) + "^" + str(v[j]))
                if j != arity-1: f.write("  x  ")
            f.write("   = " + str(rationals[i]) + "\n")

def main():
    '''
    Usage
        python3 rats.py [input_file] [output_file]
        first line of the input file contains the arity K of the vector game
        each remaining line contains the K-dimensional vector in order
    '''
    if len(sys.argv) != 3:
        print(main.__doc__)
        sys.exit(0)
    fname_in = sys.argv[1]
    arity, vectors = read_vectors(fname_in)
    rationals = to_rationals(arity, vectors)
    fname_out = sys.argv[2]
    output(arity, vectors, rationals, fname_out)
    print("Done")


if __name__ == "__main__": main()