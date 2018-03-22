			beq $a0, $a1, fdas
			j asdf
			add  $v1, $v1, $v0 # should be skipped
asdf: addi $v0, $v0, 1 # should run
			
			add  $v1, $v1, $v0 # should be skipped

# This comment should not show up on output
			li $v0, 1 # test comment
			move $a0, $v0
			syscall
fdas:
