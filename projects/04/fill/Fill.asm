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

// target = @SCREEN + 8192
@SCREEN
D=A
@8192
D=D+A
@target
M=D

// current = @SCREEN
@SCREEN
D=A
@current
M=D

// mode = off
@mode
M=-1

(DISPLAY)
// if (current == target) goto KEYHANDLER
@current
D=M
@target
D=D-M
@KEYHANDLER
D;JEQ

// draw @SCREEN + ram
@mode
D=M
@current
A=M
M=D

// current = current + 1
@current
M=M+1

// goto DISPLAY
@DISPLAY
0;JMP

(KEYHANDLER)
// if (not key-pressed) goto CLEAR
@KBD
D=M
@CLEAR
D;JEQ

// fill black
@mode
M=-1

// goto reset
@RESET
0;JMP

(CLEAR)
// fill white
@mode
M=0

(RESET)
// current = @SCREEN
@SCREEN
D=A
@current
M=D
// goto display
@DISPLAY
0;JMP
