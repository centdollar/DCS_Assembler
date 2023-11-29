

.dir

.equ matrix1 0x200
.equ matrix2 0x300
.equ resultant 0x400

.enddir


.constants


.endconstants


.code

// Matrix Multiplication of a 4x4 Matrix


addc r8 #8
sub r4 r4
// Loop to input 8 data entries
@DataInput1 addc r4 #0
in r3 r0
st r4 r3 m[matrix1]
addc r4 #1
out r3 r0
cmp r0 r8
jz0 r1 @DataInput1

@DataInput2 addc r4 #0
in r3 r0
st r4 r3 m[matrix1]
addc r4 #1
out r3 r0
cmp r0 r8
jz0 r1 @DataInput2







.endcode
