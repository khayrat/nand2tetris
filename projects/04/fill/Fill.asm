// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//row_words = 256 * 32
@8191
//@8192
D=A
@row_words
M=D

(ENDLESS_LOOP)
  // keyboard-handling
  
  //if RAM[KBD] == 0
  //  pixel_color = white
  //else
  //  pixel_color = balck
  @KBD
  D=M
  @WHITE
  D;JEQ
  @BLACK
  0;JMP

  (WHITE)
    @pixel_color
    M=0
    @DRAW
    0;JMP

  (BLACK)
    @pixel_color
    M=-1

(DRAW)
  //addr = SCREEN
  @SCREEN
  D=A
  @addr
  M=D 
  //i = 0
  @i
  M=0

  // draw-loop
  (LOOP)
    //if i > row_words goto ENDLESS_LOOP
    @i
    D=M
    @row_words
    D=D-M
    @ENDLESS_LOOP
    D;JGT

    //RAM[addr] = pixel_color
    @pixel_color
    D=M
    @addr
    A=M
    M=D

    //addr = addr + 1
    @addr
    M=M+1

    //i = i + 1
    @i
    M=M+1

    //goto LOOP
    @LOOP
    0;JMP

