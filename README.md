# MIPSim
MIPS simulator written in python3

# Installation

No additional packages are required to run this. To install simply clone the repo, navigate to the project root and run
''' python3 main.py <optional-flags> <filename> '''

# Currently supported instructions

addi
add
sub
mult
mflo
mfhi
mul

sll
srl
li
move
syscall
and
or
xor
nor
beq
bne
bgez
bgtz
blez
bltz
bgezal
bltzal
j
jal
jr
sw
lw

#Supported pseudo instructions
mul - mult and mflo
li - addi with 0
nop - do nothing

# Useful MIPS reference links
[MIPS ISA](http://www.math-cs.gordon.edu/courses/cps311/handouts-2017/MIPS%20ISA.pdf)
[MIPS syscall functions](https://courses.missouristate.edu/KenVollmar/mars/Help/SyscallHelp.html)
[MIPS directives](http://students.cs.tamu.edu/tanzir/csce350/reference/assembler_dir.html)