

.dir

.equ CONST1 3

.enddir


.constants


.endconstants


.code
sub r0 r0
sub r1 r1
sub r2 r2
addc r2 #15
nop
add r0 r2

@Loop2 nop
addc r8 #1
sub r7 r7
@Loop1 nop
st r7 r7 m[0x500]
addc r7 #1
cmp r7 #15
jz0 r1 @Loop1
call r1 @Function
call r1 @Function
cmp r8 #2
jz0 r1 @Loop2
call r1 @Function

addc r1 #5
nop
sub r0 r1

sub r10 r10
addc r10 #1
out r10 r0


@Function nop
addc r15 #1
ret


.endcode
