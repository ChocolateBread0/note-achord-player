A Python-based synthesizer that generates musical notes and chords from scratch using additive synthesis and physical modeling principles.

##How it works

The program accept a matrix of two element: note/achord, duration of the note. convert the note in a frequency using the law:

$$f = 440 \cdot 2^{(n-49)/12}$$

then create the wave, based on a superposition of sine if it's a chord (i=1,..n), a single sing if a note (i=1)

$$y(t) = \sum e^{-kt} \cdot \sin(2\pi f t)$$
