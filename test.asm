#j swtest
# random tests
		li $t1, 1
		sll $t1, $t1, 31
		li $t2, 5
		mult $t1, $t2
		mflo $a0
		li $v0, 1
		syscall

		jal newline
		
		j looptest

#		beq $a0, $a1, exit
		j asdf
		add  $v1, $v1, $v0 # should be skipped
asdf: 	addi $v0, $v0, 1 # should run
	
		add  $v1, $v1, $v0 # should be skipped

# This comment should not show up on output
		li $v0, 1 # test comment
		move $a0, $v0
		syscall

looptest:
#basic for loop
		li $t0, 0
		li $t1, 5
loopstart:
		li $v0, 1
		move $a0, $t0
		syscall

		addi $t0, $t0, 1

		jal newline
		
		bne $t0, $t1, loopstart	
		
		j exit

swtest:
		li $t0, 10
		sw $t0, 0($sp)
		lw $t1, 0($sp)

		j exit

		j endnewline
newline:
		li $v0, 11
		li $a0, '\n'
		syscall

		jr $ra
endnewline:

exit:

		li $v0, 10 # Terminate program run and
		syscall    # Exit
