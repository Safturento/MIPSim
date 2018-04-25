# MIPSim
MIPS simulator written in python3 with gui displaying 

# Installation & Usage
The only requirement is python3-tk if you wish to use the gui.
To install simply clone the repo, navigate to the project root and run
``` 
usage: main.py [-h] [-c] [-s] file_path

positional arguments:
  file_path      path to assembly file

optional arguments:
  -h, --help     show this help message and exit
  -c, --console  force cli interface instead of gui
  -s, --step     step through program line by line
```

To run through the file simply press enter once its opened, if using the ```-s``` flag press enter for each step (or hold enter to fast forward)

**Warning:** using the ```-s``` and ```-c``` flag at the same time will place code inline with output and may be messy to read. It is just suggested to use these together.

# Currently supported instructions
```
addi, add, sub, mult, mflo, mfhi, mul
sw, lw
sll, srl, and, or, xor, nor
beq, bne, bgez, bgtz, blez, bltz, bgezal, bltzal
j, jal, jr
```
note: syscall's print int and exit values are also implemented.

#Supported pseudo instructions
```
mul - mult and mflo
li - addi with 0
nop - do nothing
move - addu with 0
```

# Useful MIPS reference links
[Mips Instruction Reference](http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html)

[MIPS ISA](http://www.math-cs.gordon.edu/courses/cps311/handouts-2017/MIPS%20ISA.pdf)

[MIPS syscall functions](https://courses.missouristate.edu/KenVollmar/mars/Help/SyscallHelp.html)

[MIPS directives](http://students.cs.tamu.edu/tanzir/csce350/reference/assembler_dir.html)
