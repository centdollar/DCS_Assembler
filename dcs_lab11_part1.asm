

.dir

.equ matrix1 0x200
.equ matrix2 0x300
.equ resultant 0x400

.enddir


.constants


.endconstants


.code

// Matrix Multiplication of a 4x4 Matrix

// Correct assembly for inputing data from switches
// 
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

out r5 r0







.endcode
