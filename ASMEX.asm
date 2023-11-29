

.dir

.equ CONST1 3

.enddir


.constants

.word FIRST 0x0FFF
.word SECOND 0x0FFE

.endconstants


.code
sub r2 r2
sub r3 r3
sub r4 r4
sub r5 r5
sub r6 r6
sub r8 r8
sub r9 r9


addc r3 #8
addc r2 #2
add r6 r3
add r6 r2

call r1 @label1
addc r9 #5
@label2 subc r9 #1
jz0 r1 @label2
addc r7 #1
ld r0 r5 m[0xFFF0]


addc r2 #1

@label3 out r2 r0
in r3 r0
ju r1 @label3

@label1 div r6 r2

st r0 r6 m[0xFFF0]
addc r15 #1
ret

.endcode
