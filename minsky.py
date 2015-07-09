import argparse

commands = {}


def load_machine(fname):
    commands = {}

    def err(x): raise ValueError(x)

    with open(fname, "r") as f:
        line = f.readline()
        num_registers = int(line)
        for line in f:

            # Skip over empty lines.
            line = line.rstrip().lstrip()
            if len(line) == 0: continue

            # Get line number for this instruction.
            line = line.split()
            line_num = int(line[0])

            # Check for halting state.
            if line[1] == "HALT":
                commands[line_num] = ("HALT",)
                continue

            # Parse register number.
            register = int(line[1][1:])  # parse the X out of rXX
            if register < 1 or register > num_registers: err("Accessing unknown register.")
            oper = line[2]

            # Looks like this.
            # 1 r1 + 15
            if oper == "+":
                goto = int(line[3])
                commands[line_num] = (oper, register, goto)

            # Looks like this.
            # 2 r1 - >0 10 =0 5
            elif oper == "-":
                if not line[3] == ">0": err("expected >0")
                gt0 = int(line[4])
                if not line[5] == "=0": err("expected =0")
                eq0 = int(line[6])
                commands[line_num] = (oper, register, gt0, eq0)

            # Parsing error.
            else:
                err("Unknown operation")
    return commands, [0] * num_registers


def run_machine(instructions, registers, machine_in, trace=None):
    registers[0] = machine_in
    line = 1
    print("Input: {}".format(registers))
    while True:

        # Get instruction to execute. Check for halting state.
        instr = instructions[line]
        oper = instr[0]
        if oper == "HALT":
            if trace: print("{} \t HALT".format(registers))
            break

        # Registers are indexed from 1.
        i = instr[1] - 1

        # Execute "+" or "-" operation.
        if oper == "+":
            registers[i] += 1
            goto = instr[2]
            if trace: print("{} \t Add 1 to r{}, goto {}".format(registers, i, goto))
        elif oper == "-":
            if registers[i] > 0:
                registers[i] -= 1
                goto = instr[2]
                if trace: print("{} \t Sub 1 from r{}, goto {}".format(registers, i, goto))
            else:
                goto = instr[3]
                if trace: print("{} \t r{} is empty, goto {}".format(registers, i, goto))

        # Next line to execute.
        line = goto
    print("Output: {}".format(registers))



def main():
    # parse arguments.
    parser = argparse.ArgumentParser("A minsky machine simulator.")
    parser.add_argument("--machine", required=True, help="File to read machine from.")
    parser.add_argument("--input", required=True, type=int, help="Input to feed the machine.")
    parser.add_argument("--trace", required=False, type=bool, help="Whether to trace each step of machine.")
    args = parser.parse_args()

    # load machine.
    instructions, registers = load_machine(args.machine)
    run_machine(instructions, registers, int(args.input), trace=args.trace)

if __name__ == "__main__":
    main()


