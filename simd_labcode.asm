.dir

.equ Vect_addend 2
.equ lower_array 0x2000
.equ upper_array 0x2100
.equ decimal_array 0x2200
.equ converted_to_upper 0x2050
.equ converted_to_lower 0x2150
.equ converted_decimal 0x2250

.enddir


.constants

// starting values for upper,lower,decimal vectors
// ex: [1000001, 1000010] = ['A','B']
.word CAP 0x3FFF 10000011000010
.word LOW 0x3FFE 11000011100010
.word NUM 0x3FFD 01100000110001

.endconstants

.code
@start sub r5 r5
sub r6 r6

sub r3 r3
sub r4 r4
sub r15 r15



addc r6 #2



// SECTION 0
// creates array with the lowercase chars starting at address 0x0200
ld r0 r5 m[LOW]
addc r3 #13
@LowerCase addc r4 #0
st r4 r5 m[lower_array]
addc r4 #1
vaddc r5 Vect_addend
subc r3 #1
jz0 r1 @LowerCase

sub r5 r5
sub r3 r3
sub r4 r4
addc r15 #1
out r15 r0
//



// SECTION 1
// creates array with the uppercase chars starting at address 0x0400
ld r0 r5 m[CAP]
addc r3 #13
@UpperCase addc r4 #0
st r4 r5 m[upper_array]
addc r4 #1
vaddc r5 Vect_addend
subc r3 #1
jz0 r1 @UpperCase

add r15 #0
sub r5 r5
sub r3 r3
sub r4 r4
addc r15 #1
out r15 r0


//


// SECTION 2
// creates array with the number chars starting at address 0x0600
ld r0 r5 m[NUM]
addc r3 #5
@NumCase addc r4 #0
st r4 r5 m[decimal_array]
addc r4 #1
vaddc r5 Vect_addend
subc r3 #1
jz0 r1 @NumCase


addc r15 #0
sub r5 r5
sub r3 r3
sub r6 r6
sub r4 r4
addc r15 #1
out r15 r0



//


// SECTION 3
// Turn lower case letters into upper case ones
// upper = lower - 10000 
// setup lower 10000 in a register
addc r9 #8
rotl r9 #2

// needed because we pre increment
ld r3 r5 m[lower_array]
vsub r5 r9
st r3 r5 m[converted_to_upper]

@lowerToUpper addc r15 #0
addc r3 #1
ld r3 r5 m[lower_array]
vsub r5 r9
st r3 r5 m[converted_to_upper]
cmp r3 #13
jz0 r1 @lowerToUpper

addc r15 #0
sub r3 r3
addc r15 #1
out r15 r0


// SECTION 4
// needed because we pre increment
ld r3 r5 m[upper_array]
vadd r5 r9
st r3 r5 m[converted_to_lower]

@upperToLower addc r15 #0
addc r3 #1
ld r3 r5 m[upper_array]
vadd r5 r9
st r3 r5 m[converted_to_lower]
cmp r3 #13
jz0 r1 @upperToLower

addc r15 #0
sub r9 r9
addc r9 #12
rotl r9 #2

sub r3 r3
addc r15 #1
out r15 r0



// SECTION 5
// needed because we pre increment
ld r3 r5 m[decimal_array]
vsub r5 r9
st r3 r5 m[converted_decimal]

@convDecimal addc r15 #0
addc r3 #1
ld r3 r5 m[decimal_array]
vsub r5 r9
st r3 r5 m[converted_decimal]
cmp r3 #4
jz0 r1 @convDecimal

addc r13 #0
addc r15 #1
out r15 r0
.endcode 