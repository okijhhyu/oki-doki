.data
	true: .byte 1
	false: .byte 0
	str0: .asciiz "sin("
	str1: .asciiz "):="
	str2: .asciiz ";\n"
.text
main:
	li $s1, 0
	li $s0, 91
	li.s $f13, 0.0
	li.s $f14, 0.0
L0:
	la $t0, false
	bge $s1, $s0, SKIP0
	la $t0, true
SKIP0:
	la $t1, true
	beq $t1, $t0, if0
	j L1
L1:
	j END
if0:
	li $t1, 1
	addu $t1, $s1, $t1
	move $s1, $t1
	li.s $f0, 4.0
	mul.s $f0, $f0, $f13
	li.s $f4, 180.0
	sub.s $f1, $f4, $f13
	mul.s $f2, $f0, $f1
	mov.s $f14, $f2
	li.s $f4, 180.0
	sub.s $f0, $f4, $f13
	mul.s $f1, $f13, $f0
	mov.s $f15, $f1
	li.s $f0, 40500.0
	sub.s $f0, $f0, $f15
	div.s $f1, $f14, $f0
	mov.s $f14, $f1
	li $v0, 4
	la $a0, str0
	syscall
	li $v0, 2
	mov.s $f12, $f13
	syscall
	li $v0, 4
	la $a0, str1
	syscall
	li $v0, 2
	mov.s $f12, $f14
	syscall
	li $v0, 4
	la $a0, str2
	syscall
	li.s $f1, 1.0
	add.s $f0, $f13, $f1
	mov.s $f13, $f0
	j L0
END:
