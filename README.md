# DMX Drums

This is a small project that I put together because I bought a stage light on Amazon many years ago and wondered if it would be possible
to control with MIDI drum pads using the DMX port and a Raspberry PI. It turns out that it is indeed possible and actually not too complicated.

This was made especially possible thanks to the dmx485 project here:
https://github.com/bitbyt3r/dmx

which was one of the most straightforward implementations of controlling a light via pyserial that I could find. I do not have any experience with stage lights or DMX, but just looking through the code (and tinkering with various other libraries too) helped me to understand what is going on.

For those interested, basically, we are constantly sending 512 8-bit numbers to the light. The light operates on a particular channel, which can be
chosen on the back of the light (at least for the one that I am using). Let's say the selected channel is "1". Now, the next four channels will control the color (the first is intensity and the remaining three are color).

It took lots of experimentation to realize which values worked, whereas other libraries would assume that the first three channels are RGB. I am not sure if there is some official documentation, but it was especially fun to experiment with different values and find out what happens.

There seemingly are other values that control other aspects of the light, such as pulse width (I think is the fifth channel?)

Anyway, this was a fun project and if anybody finds this on the internet and wants to do something similar, maybe this will help inspire you.