# Ring-Buffer-Implementation-for-Audio
Hi welcome to my "Ring Buffer Project" for CSPB 2244 Data Structures course at CU Boulder in the summer of 2024.
The goal of this project was to implement a Ring Buffer data structure and explore its potential for live audio 
processing. The structure is implemented in python.

A ring buffer is a fixed sized array with two pointers, a head and a tail. It is cicular in nature so the pointers 
wrap around to the beggining of the array when they go past the final element. The head points to the oldest element
at all times and the tail to the position where the newest will be inserted. This allos for FIFO operations. Insertions
and removals are done in costant time. A ring buffer can be implimented to overwrite old data or reject new data until old
data has been popped from the array. I played around with both types of implimentations during the course of this project. 

A ring buffer is potentially useful in live audio processing for the following reasons. It can handle a continious flow of
data. Its contant time operations are fast. The array is a fixed size and can therefore be used to chuck the data into smaller 
in order to proccess the audio quickly without doing too many computations. The circular nature of this structure also lends itself 
to looping audio effects like: delays, reverb and other spacial effects. Unfortunetly, I have been unable to get a spacial 
effect working with my ring buffer structure. However, in the process I learned alot about how audio data is processed. 
My biggest challenge came in linking my structure up to python's stadard library wave module. This module helps with reading 
and writing audio in .wav but also packing/unpacking it into sequences of values as well as handling multiple channels of audio.
This was my biggest frustration during this project because I was able to see the delayed values vs the undelayed ones and I was 
also able to see the result of them being added together. However, I could consistently get my output files to create a 
echo effect. At one point a did have echo and even sustain on the echo functioning. But I was quickly unable to produce those result.
Having not changed my code at all between that change of result I was baffled. I think with more time I could have more throurouly 
investigated the wave module. Unfortunely, running short on time I had to press pause and evaluate what I had accomplished
and it is included here in this repository. 

There is the "TestingBuffer.py" which shows the buffer implimentation seperate from any audio processing. 
It has a main function that demonstrates the buffer is working properly.

There is also "EchoDelay.py" which reads, processes and writes a inputed .wav file. Alas while it reads 
and writes fine, the effect is not function but it shows what I was attempting to accomplish. 
Audio (.wav) files must of course be contained in the same folder as the code in-order for the code to read
them. The code outputs a effected copy of the audio to the that same directory. 
