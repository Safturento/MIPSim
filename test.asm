			j asdf
			add  $v1, $v1, $v0 # shuold be skipped
asdf: addi $v0, $v0, 1 # should run

# This comment should not show up on output
			li $v0, 1 # test comment
			move $a0, $v0
			syscall
