		.data
exit:	.asciiz "exiting"
		.text
		.globl main
main:	
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
		li $a0, 0
		li $t0, 5
		li $v0, 1

start:
		addi $a0, $a0, 1
		syscall
		bne $a0, $t0, start

exit:
		li $v0, 10 # Terminate program run and
		syscall    # Exit