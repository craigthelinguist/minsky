# Minsky Machine.
A Minsky machine (aka a register machine) is a model of computation. It has a finite number of registers and labelled instructions. There are three kinds of instructions:
* Add 1 to a register and goto a line.
* Check if a register contains a value greater than 0. If it does, subtract 1 and goto a line. If it doesn't, do nothing and goto another line.
* Halt computation.

To run a Minsky machine on input *x*, the machine is started with register 1 containing *x* and the rest containing 0. The output of a Minsky machine is the value in register 1 when it halts.

# The Simulation.

Programs to a Minsky machine are specified in .minsky files. They can be run like so:

```bash
python3 minsky.py --machine is_odd.minsky --input 2
```

This means "run the program is_odd on input 2":

```bash
Input: [2]
Output: [1]
```

There is an optional flag, *trace*, which you can use to see what the machine is doing step-by-step.

```bash
python3 minsky.py --machine is_odd.minsky --input 5 --trace True
Input: [2]
[1] 	 Sub 1 from r0, goto 2
[0] 	 Sub 1 from r0, goto 1
[0] 	 r0 is empty, goto 3
[1] 	 Add 1 to r0, goto 4
[1] 	 HALT
Output: [1]
```
