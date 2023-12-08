

.dir

.equ matrix1 0x500
.equ matrix2 0x600
.equ resultant 0x700
.equ intermediate 0x800

.enddir


.constants


.endconstants


.code


// Input the two matrix
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
// End of the input phase from the switches

// Start of matrix multiplication last two rows
// Multiply a matrix take 3!!
// main loop iterator
sub r0 r0
addc r0 #3

// Row Data register
sub r1 r1
sub r2 r2
sub r3 r3
sub r4 r4
// row index reg
sub r5 r5
addc r5 #4

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

nop
ld r5 r1 m[matrix1]
addc r5 #1
nop
ld r5 r2 m[matrix1]
addc r5 #1
nop
ld r5 r3 m[matrix1]
addc r5 #1
nop
ld r5 r4 m[matrix1]
addc r5 #1

@ColLoop nop
ld r11 r6 m[matrix2]
addc r11 #4
nop
ld r11 r7 m[matrix2]
addc r11 #4
nop
ld r11 r8 m[matrix2]
addc r11 #4
nop
ld r11 r9 m[matrix2]
addc r11 #4
nop

cpy r12 r1
nop
cpy r13 r2
nop
cpy r14 r3
nop
cpy r15 r4
nop

mul r6 r12
nop
mul r7 r13
nop
mul r8 r14
nop
mul r9 r15

add r12 r13
add r12 r14
add r12 r15
nop
sub r13 r13
sub r14 r14
addc r13 #4
addc r14 #4
nop
sub r14 r0
nop
mul r14 r13
nop
sub r14 r14
addc r14 #4
nop
sub r14 r10
nop
add r14 r13

nop
st r14 r12 m[resultant]
nop



subc r11 #15
subc r10 #1
jz0 r1 @ColLoop
nop

sub r11 r11
addc r11 #1
nop
addc r10 #4
nop


nop
nop

// End of matrix multiplication, last two rows



// Core communication stuff
// send a 1 out to tell the other core that next data will be valid


sub r4 r4
sub r5 r5
sub r6 r6
sub r13 r13
addc r13 #1
addc r6 #4

addc r4 #4


// Make this into a loop for more readable code

@SendResultToC0 nop
nop
// load the result to be sent out
ld r6 r5 m[resultant]
addc r6 #1
nop


// Present the data and ack sig to Core0
// r1 is the ack to core 0
out r13 r1
out r5 r2

// wait until core 0 sends that it got the data
@waitforcore1 nop
in r15 r1
nop
nop
rrz r15 #1
jz0 r1 @waitforcore1
nop
nop
subc r4 #1
jz0 r1 @SendResultToC0



// To receive from core 0, commented out becuase only core 1 sends to core 0
// @rxfrom0 nop
// in r5 r1
// nop
// nop
// rrz r5 #1
// jz1 r1 @rxfrom0
// nop
// grab data from other core
// in r6 r2


@done nop
nop
ju r1 @done



.endcode
