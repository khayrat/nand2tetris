// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//a = R0
@R0
D=M
@a
M=D

//b = R1
@R1
D=M
@b
M=D

//prod = 0
@prod
M=0

//LOOP:
(LOOP)
  //  if b == 0 goto STOP
  @b
  D=M
  @STOP
  D;JEQ

  //  prod = prod + a
  @a
  D=M
  @prod
  M=M+D

  //  b = b - 1
  @b
  M=M-1

  //  goto LOOP
  @LOOP
  D;JMP

//STOP:
(STOP)
  //  R2 = prod
  @prod
  D=M
  @R2
  M=D

(END)
  @END
  0;JMP 
