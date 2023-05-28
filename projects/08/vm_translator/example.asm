// SP=256 (offset)
@256
D=A
@0
M=D
// RAM[256] = 7
//   D=7
@7
D=A
@SP
A=M
M=D
// inc sp
@0
M=M+1
// RAM[257] = 8
//   D=8
@8
D=A
@SP
A=M
M=D
// inc sp
@0 
M=M+1
// add
// pop to D 
// dec sp
@SP
M=M-1
// D = RAM[SP]
A=M
D=M
// pop to A
// dec sp
@SP
M=M-1
// A = RAM[SP]
A=M
A=M
// D+A
D=D+A
// push D 
@0
A=M
M=D
@0
M=M+1
