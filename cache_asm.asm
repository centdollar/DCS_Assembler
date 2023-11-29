

.dir

.equ CONST1 3

.enddir


.constants

.word CAP 0x3FFF 10000011000010
.word LOW 0x3FFE 11000011100010
.word NUM 0x3FFD 00000000110000

.endconstants


.code
@start sub r5 r5
sub r6 r6
sub r3 r3
sub r4 r4



addc r6 CONST1




// creates array with the lowercase chars starting at address 0x0200
ld r0 r5 m[LOW]
addc r3 #13
@LowerCase addc r4 #0
st r4 r5 m[0x2000]
addc r4 #1
vadd r5 r6
subc r3 #1
jz0 r1 @LowerCase

sub r5 r5
sub r3 r3
sub r4 r4

// creates array with the uppercase chars starting at address 0x0400
ld r0 r5 m[CAP]
addc r3 #13
@UpperCase addc r4 #0
st r4 r5 m[0x2100]
addc r4 #1
vadd r5 r6
subc r3 #1
jz0 r1 @UpperCase


sub r5 r5
sub r3 r3
sub r4 r4

// creates array with the number chars starting at address 0x0600
ld r0 r5 m[CAP]
addc r3 #9
@NumCase addc r4 #0
st r4 r5 m[0x2200]
addc r4 #1
vadd r5 r6
subc r3 #1
jz0 r1 @NumCase


sub r5 r5
sub r3 r3
sub r6 r6
sub r4 r4

// attempting to cause writeback from cache by loading a bunch or random memory locations
// To do this start with a block address of 64, so 8*64 for actual address, then loop 16 times adding 8 to actual address, may need to move where I am storing the arrays to a later place in memory
sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads1 addc r6 #0
ld r4 r10 m[0x0100]
addc r4 #8
subc r6 #1
jz0 r1 @loads1


sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads2 addc r6 #0
ld r4 r10 m[0x0200]
addc r4 #8
subc r6 #1
jz0 r1 @loads2

sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads3 addc r6 #0
ld r4 r10 m[0x0300]
addc r4 #8
subc r6 #1
jz0 r1 @loads3


sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads4 addc r6 #0
ld r4 r10 m[0x0400]
subc r6 #1
jz0 r1 @loads4

sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads5 addc r6 #0
ld r4 r10 m[0x0500]
subc r6 #1
jz0 r1 @loads5


sub r6 r6
sub r4 r4
addc r6 #4
addc r4 #8
@loads6 addc r6 #0
ld r4 r10 m[0x0600]
subc r6 #1
jz0 r1 @loads6

sub r12 r12

ju r0 @start


.endcode
