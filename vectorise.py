
import sys

def construct_minsky(f_in):
    '''
    Construct a Minsky machine from the specified file.
    :param f_in: name of file to read
    :return: number of registers, map of line num -> instruction
    '''
    with open(f_in, "r") as f:
        num_registers = int(f.readline().lstrip().rstrip())
        instructions = {}
        for line in f:
            line = line.split()
            line_num = int(line[0])
            instruction = line[1:]
            instructions[line_num] = instruction
        return num_registers, instructions

def instruction_to_vector(num_registers, line, args):
    '''
    Given a line and its constuction, return a list of the corresponding vectors
    :param line: the line that this instruction is.
    :param args: the rule for what this line does.
    :return:
    '''
    v = None
    as_bin = lambda x : 1 if x else 0

    # halt execution
    if args[0] == "stop":
        return [([0] * num_registers) + [-line, 0]]

    # incrementing a registry
    elif args[0][-1] == "+":
        r = int(args[0][1]) - 1 # will look like r3+, get middle element
        next_state = int(args[1])
        return [[as_bin(i==r) for i in range(num_registers)] + [-line, next_state]]

    # decrementing a registry
    # note that this corresponds to two states
    elif args[0][-1] == "-":
        r = int(args[0][1]) - 1 # will look liKe r3-, get middle element
        t1 = int(args[2]) # transition state if r3 > 0
        t2 = int(args[4]) # transition state if 43 = 0
        v1 = [-as_bin(i==r) for i in range(num_registers)] + [-line, t1]
        v2 = [0]*num_registers + [-line, t2]
        return [v1, v2]

    # malformed instructions
    else:
        print("Parse error: unknown action " + args[0])
        sys.exit(1)

def construct_game(num_registers, machine):
    '''
    Construct a vector game from a Minsky machine.
    :param num_registers: number of registers in the Minsky.
    :param machine: map of line number -> instruction, int -> str
    :return:( int, [[int]]) the arity of game and list of vectors
    '''

    # the registers have their order reversed in the vector game
    order = reversed(sorted(machine.keys()))
    vectors = []
    for line in order:
        vectors += instruction_to_vector(num_registers, line, machine[line])
    control_instruction = [0] * num_registers + [1,-1]
    return num_registers + 2, [control_instruction] + vectors

def output(arity, game, f_out):
    '''
    Output the vector game with specified arity to f_out.
    :param arity: number of components in each vector.
    :param game: list of vectors [[int]]
    :param f_out: name of file
    '''
    with open(f_out, "w") as f:
        f.write(str(arity) + "\n")
        for v in game:
            for i, val in enumerate(v):
                f.write(str(val))
                if i != arity-1: f.write("\t")
            f.write("\n")

def main():
    '''
    Usage:
        python3 minsky.py [file_in] [file_out]

        file_in is a line containing the number of registers.
        each successive line corresponds to an instruction.
        an example of each of the three kinds of instructions:

          1) Instruction 5: increment register 3, go to instruction 8.
                5 r3+ 8
          2) Instruction 12: if register 2 > 0, decrement register 2 and go to
             instruction 13. Else go to instruction 15.
                12 r2- >0 13 =0 15
          3) Instruction 20: stop execution.
                15 stop
    :return:
    '''
    if len(sys.argv) != 3:
        print(main.__doc__)
        sys.exit(0)
    f_in = sys.argv[1]
    num_registers, machine = construct_minsky(f_in)
    arity, vector_game = construct_game(num_registers, machine)
    f_out = sys.argv[2]
    output(arity, vector_game, f_out)
    print("Done")

if __name__ == "__main__": main()
