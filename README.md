A Python-based synthesizer that generates musical notes and chords from scratch using additive synthesis and physical modeling principles.

## How it works

The program accepts a matrix of two elements: note/chord and duration. It converts the note into a frequency using the law:

$$f = 440 \cdot 2^{(n-49)/12}$$

Then, it creates the wave based on a superposition of sines if it's a chord ($i=1,..,n$), or a single sine if it's a note ($i=1$):

$$y(t) = \sum e^{-kt} \cdot \sin(2\pi f t)$$
