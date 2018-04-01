.data
		.asciiz "test string"
.text
		li $v0, 'a'
		beq $a0, $a1, fdas
		j asdf
		add  $v1, $v1, $v0 # should be skipped
asdf: 	addi $v0, $v0, 1 # should run
		
		
		add  $v1, $v1, $v0 # should be skipped

# This comment should not show up on output
		li $v0, 1 # test comment
		move $a0, $v0
		syscall
fdas:

#basic for loop
		li $t0, 0
		li $t1, 5
loopstart:
		li $v0, 1
		move $a0, $t0
		syscall

		addi $t0, $t0, 1

		li $v0, 11
		li $a0, '\n'
		syscall
		
		bne $t0, $t1, loopstart
		
		nop
		nop
		nop

		li $v0, 10 # Terminate program run and
		syscall    # Exit
