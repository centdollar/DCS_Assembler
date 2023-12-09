

.dir

.equ matrix1 0x500
.equ matrix2 0x600
.equ resultant 0x700
.equ intermediate 0x800

.enddir


.constants


.endconstants


.code

// Matrix Multiplication of a 4x4 Matrix

// Correct assembly for inputing data from switches
// Need to Loop 16 Times now and store it into memory

sub r15 r15
sub r14 r14
addc r15 #15
addc r15 #1
nop

@InputLoop nop

@waitForPressed nop
in r5 r0
nop
nop
rrz r5 #1
jz1 r1 @waitForPressed

nop
nop

@waitForUnpressed nop
in r5 r0
nop
nop
rrz r5 #1
jz0 r1 @waitForUnpressed

nop
st r14 r5 m[matrix1]

nop
nop


out r5 r0
addc r14 #1

subc r15 #1
jz0 r1 @InputLoop

nop
nop

sub r15 r15
sub r14 r14
addc r15 #15
addc r15 #2
nop

@InputLoop1 nop

@waitForPressed1 nop
in r5 r0
nop
nop
rrz r5 #1
jz1 r1 @waitForPressed1

nop
nop

@waitForUnpressed1 nop
in r5 r0
nop
nop
rrz r5 #1
jz0 r1 @waitForUnpressed1

nop
nop
st r14 r5 m[matrix2]

nop
nop


out r5 r0
addc r14 #1

subc r15 #1
jz0 r1 @InputLoop1

nop
nop
nop

// Multiply a matrix take 3!!
// main loop iterator
sub r0 r0
addc r0 #4

// Row Data register
sub r1 r1
sub r2 r2
sub r3 r3
sub r4 r4
// row index reg
sub r5 r5

// Col data registers
sub r6 r6
sub r7 r7
sub r8 r8
sub r9 r9
// row iterator reg
sub r10 r10
addc r10 #4
// row index reg
sub r11 r11
addc r11 #1


@RowCalc nop
ld r5 r1 m[matrix1]
addc r5 #1
ld r5 r2 m[matrix1]
addc r5 #1
ld r5 r3 m[matrix1]
addc r5 #1
ld r5 r4 m[matrix1]
addc r5 #1

@ColLoop nop
ld r11 r6 m[matrix2]
addc r11 #4
ld r11 r7 m[matrix2]
addc r11 #4
ld r11 r8 m[matrix2]
addc r11 #4
ld r11 r9 m[matrix2]
addc r11 #4

cpy r12 r1
cpy r13 r2
cpy r14 r3
cpy r15 r4

mul r6 r12
mul r7 r13
mul r8 r14
mul r9 r15

add r12 r13
add r12 r14
add r12 r15
sub r13 r13
sub r14 r14
addc r13 #4
addc r14 #4
sub r14 r0
mul r14 r13
sub r14 r14
addc r14 #4
sub r14 r10
add r14 r13

st r14 r12 m[resultant]



subc r11 #15
subc r10 #1
jz0 r1 @ColLoop

sub r11 r11
addc r11 #1
addc r10 #4


subc r0 #1
jz0 r1 @RowCalc


sub r10 r10
@displayResult nop
ld r10 r9 m[resultant]
addc r10 #1
cmp r10 #15
jz0 r1 @displayResult





sub r10 r10
nop
addc r10 #5
nop
out r10 r0

@done nop
nop
nop
ju r1 @done


.endcode
