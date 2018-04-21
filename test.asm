			#initialize loop
			addi $t0, $0, 5
			addi $t2, $0, 1

			# left shift and store value
loopstart:
			sll $t2, $t2, 1
			
			sw $t2, 0($sp)
			addi $sp, $sp, 4

			#iterate and check
			addi $t1, $t1, 1
			beq $t0, $t1, loopend
			j loopstart
loopend:


			#initialize loop 
			addi $t1, $0, 5

printloop:
			#load and print
			addi $v0, $0, 1
			
			addi $sp, $sp, -4
			lw $a0, 0($sp)
			syscall 

			jal printreturn

			#iterate and check
			addi $t1, $t1, -1
			blez $t1, endprintloop
			j printloop
endprintloop:


			# simple function to 
			# print return statement
			j returnend
printreturn:
			addi $v0, $0, 11
			addi $a0, $0, '\n'
			syscall

			jr $ra
returnend:
			
exit:
			addi $v0, $0, 10
			syscall
