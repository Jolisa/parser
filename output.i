 loadI  1024  =>  r0 
 loadI  128  =>  r3 
 loadI  32  =>  r6 
 loadI  1028  =>  r11 
 mult  r6,  r6  =>  r10 
 rshift  r6,  r10  =>  r9 
 lshift  r6,  r9  =>  r8 
 add  r8,  r9  =>  r7 
 sub  r6,  r7  =>  r5 
 store  r5  =>  r4 
 load  r4  =>  r2 
 add  r2,  r3  =>  r1 
 nop 
 store  r1  =>  r0 
 output  1024 
