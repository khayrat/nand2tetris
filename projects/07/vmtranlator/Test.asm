// ### BEGIN push constant 1
// BEGIN D = 1
@1
D = A
// END D = 1
// BEGIN push D: RAM[SP++] = D
// BEGIN RAM[SP] = D
@SP
A=M
M=D
// END   RAM[SP] = D
// BEGIN SP++
@SP
M=M+1
// END   SP++
// END   push D: RAM[SP++] = D
// ### END push constant 1
// ### BEGIN push constant 2
// BEGIN D = 2
@2
D = A
// END D = 2
// BEGIN push D: RAM[SP++] = D
// BEGIN RAM[SP] = D
@SP
A=M
M=D
// END   RAM[SP] = D
// BEGIN SP++
@SP
M=M+1
// END   SP++
// END   push D: RAM[SP++] = D
// ### END push constant 2
// ### BEGIN add:
// pop R13: RAM[R13] = RAM[--SP]:
// BEGIN pop D = RAM[--SP]
// BEGIN --SP
@SP
M=M-1
// END --SP
// BEGIN D = RAM[SP]
A=M
D=M
// END D = RAM[SP]
// END pop D = RAM[--SP]
// BEGIN R13 = D
@R13
M=D
// END R13 = D
// BEGIN pop D = RAM[--SP]
// BEGIN --SP
@SP
M=M-1
// END --SP
// BEGIN D = RAM[SP]
A=M
D=M
// END D = RAM[SP]
// END pop D = RAM[--SP]
// D = D add R13: D = D add RAM[R13]: 
//  A = RAM[R13]:
@R13
A=M
//  D = D add A
D=D+A
// BEGIN push D: RAM[SP++] = D
// BEGIN RAM[SP] = D
@SP
A=M
M=D
// END   RAM[SP] = D
// BEGIN SP++
@SP
M=M+1
// END   SP++
// END   push D: RAM[SP++] = D
// ### END   add:
