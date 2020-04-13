// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

a = R0
b = R1
prod = 0


LOOP:
  if b > 0 goto STOP
  prod = prod + a
  b = b - 1
  goto LOOP

STOP:
  R2 = prod

