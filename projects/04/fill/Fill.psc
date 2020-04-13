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

// rows: 256
// pixels per row: 512
// words per row: 512/16 = 32

ROW_WORDS = 256 * 32
while (true) {
  // read keyboard
  if (key_pressed)
    pixel_color = black
  else
    pixel_color = white
  
  for (i=0; i<ROW_WORDS; i++) {
    draw line i in pixel_color
  }
}

// draw-loop
for (i=0; i<ROW_WORDS; i++) {
  draw line i in pixel_color
}

addr = SCREEN
row_words = 256 * 32
pixel_color = balck
i = 0

LOOP:
  if i > row_words goto ENDLESS_LOOP
  RAM[addr] = pixel_color
  addr = addr + 1
  i = i + 1
  goto LOOP

// keyboard-handling
kbd_addr = KBD
if RAM[kbd_addr] == 0
  pixel_color = white
else
  pixel_color = black

ENDLESS_LOOP:
  // keyboard-handling
  // draw-loop
