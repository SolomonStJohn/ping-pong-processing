# Ring-Buffer-Implementation-for-Audio
Hi, welcome to my "Ring Buffer Project" for the CSPB 2244 Data Structures course at CU Boulder in the summer of 2024. The goal of this project was to implement a ring buffer data structure and explore its potential for live audio processing. The structure is implemented in Python.

A ring buffer is a fixed-size array with two pointers: a head and a tail. It is circular in nature, so the pointers wrap around to the beginning of the array when they go past the final element. The head points to the oldest element at all times, and the tail to the position where the newest element will be inserted. This allows for FIFO operations. Insertions and removals are done in constant time. A ring buffer can be implemented to overwrite old data or reject new data until space is freed in the array. I explored both types of implementations during the course of this project.

A ring buffer is potentially useful in live audio processing for the following reasons: it can handle the continuous flow of data, and its constant-time operations are fast. The array is a fixed size and can therefore be used to chunk the data into smaller pieces to process the audio quickly without excessive computations. The circular nature of this structure also lends itself to looping audio effects like delays, reverb, and other spatial effects. Unfortunately, I have been unable to get a spatial effect working using my ring buffer structure. However, in the process, I learned a lot about how audio data is processed. My biggest challenge came in linking my data structure to Python's standard library "wave" module. This module helps with reading and writing audio in .wav format. I spent a lot of time trying to understand the logic of how audio data is stored, packed and unpacked. I got very frustrated at points because I was able to see the delayed values versus the undelayed ones and the result of their combination. However, I could not consistently get my output files to create an echo effect. At one point, I did have echo and even sustain on the echo functioning, but I struggled to replicate those results. I was baffled because several consecutive outputs were very different, even when I didn't alter the input file or the code. I think with more time, I could more thoroughly investigate the wave module. Hopefully, the contents of this repository will provide a glimpse into what I was striving to accomplish.

In the repository there is "TestBuffer.py," which shows the buffer implementation separate from any attempts at audio processing. It has a main function that demonstrates how the buffer is working properly.

There is also "EchoDelay.py," which reads, processes, and writes an input .wav file. Alas, while it reads and writes fine, the delay effect is not functional. Audio (.wav) files must, of course, be contained in the same folder as the code in order for the code to read them. The code outputs an processed copy of the audio to that same directory.

I have included a .wav file called "Bassline.wav" for use with EchoDelay.py if you wish to test its read an write capability. 
