
.dir

.equ Vect_addend 2

.enddir


.constants

.word CAP 0x3FFF 10000011000010

.endconstants

.code

sub r3 r3
sub r4 r4
sub r5 r5

addc r5 #15


// two consecutive loads with immediate addressing mode
ld r0 r3 m[0x0100]
ld r0 r4 m[0x0200]

out r5 r0



.endcode 