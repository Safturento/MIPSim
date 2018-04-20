			move $0, $0

			j skip
jumpback:
			j exit
skip:

			addi $t0, $0, 5
loopstart:

			addi $t1, $t1, 1
			beq $t0, $t1, loopend
			j loopstart
loopend:

			beq $v0, $v1, jumpback
			
exit:
			addi $v0, $0, 10
			syscall
