import wave                 
import struct

"""
The ring buffer class is a array with a head and tail pointer.
It takes size as a parameter which prepopulates the buffer of that size with 0s.
The invarients of this imlementation are that head will point to the oldest element in 
buffer. While Tail will point to the place where the newest element is to be inserted.
If tail or head reach the end of the array they warp back to the begging.
This ring buffer is stores integers since it is designed for proccessing audio data.
"""
class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size
        self.head = 0
        self.tail = 0
        self.count = 0  

    """
    This is just a member function to check values in the buffer it has no bearing on the
    audio processing. It takes an index.
    """
    def getValueAt(self, index):
        if 0 <= index < self.size:
            return self.data[index]
        else:
            raise IndexError("no such index")

    """
    This member function inserts the passed value at the index pointed to by tail and increments the tail
    pointer wrapping it back to index 0 if it reached the end of the buffer. The insert fails if the buffer is full.
    """
    def insertToBuffer(self, value):
        if self.count < self.size:
            self.data[self.tail] = value
            self.tail = (self.tail + 1) % self.size
            self.count += 1
            return True       
        else:
            return False 

    """
    This is an insert that overwrites with then passed value at the index pointed to by tail. It increments the head if the buffer
    is full to ensure that the head continues to point to the oldest value. It wraps either head and/or tail if necessary.
    """
    def insertToBufferOver(self, value):
        self.data[self.tail] = value
        self.tail = (self.tail + 1) % self.size
        if self.count == self.size:
            self.head = (self.head + 1) % self.size
        else:
            self.count += 1
        return True
            
    """
    This member function returns the value at index pointed to by head and sets the value at that index to 0.
    Then it increments head wrapping it if necessary.
    """
    def popFromBuffer(self):
        if self.count == 0:
            return 0
        value = self.data[self.head]
        self.data[self.head] = 0
        self.head = (self.head + 1) % self.size
        self.count -= 1
        return value
        
    """
    This helper function prints the values in the buffer, the size of the buffer and the indices 
    that head and tail are pointing to. It is a debugging function. 
    """
def printBuffer(buffer):
    print(f"Buffer: {buffer.data}")
    print(f"Head: {buffer.head}, Tail: {buffer.tail}, Count: {buffer.count}")
    print()
    
    """
    This helper function relies on the wave module to open a .wav file to be processed.
    It takes the name of .wav file as a parameter.
    """
def openInputFile(input_filename):
    try:
        wf = wave.open(input_filename, 'rb')
        return wf
    except IOError as error:
        print(f"Input error: {error}")
        return None

    """
    This helper function relies on the wave module to generates a "container" object for the processed data to be placed in.
    It takes as parameters the name of the output file, the number of channels (stereo is standard), the sample width (bit depth), 
    and framerate (how many bits are proccessed a second)
    """
def openOutputFile(output_filename, channels, sample_width, framerate):
    try:
        output_wf = wave.open(output_filename, 'wb')
        output_wf.setnchannels(channels)
        output_wf.setsampwidth(sample_width)
        output_wf.setframerate(framerate)
        return output_wf
    except IOError as error:
        print(f"Output error: {error}")
        return None
        
    """
    This helper function takes as prameters a file name and a new extension. 
    It removes the old extension and places a new one on the file.
    """
def removeExtensionAndAdd(filename, new_extension):
    base_name = filename.rsplit('.', 1)[0]
    new_name = base_name + new_extension
    return new_name

"""
MAIN FUNCTION
"""
def main():
    print("ECHO DELAY")
    print("♪♪------♪♪")

    chunk_size = 1024                                   # define chunck size to be processed at a time
    channels = 2                                        # set stereo audio
    sample_width = 2                                    # 16-bit sampling (2 bytes per sample)
    framerate = 44100                                   # set framerate (frames per second)
    volume_factor = 0.8                                 # scales volume of dry signal
    scaling_factor = 0.7                                # scales volume of the delayed signal (wet signal)
    feedback = 0.9                                      # feedback amount for delay sustain (0.0 to 1.0)
    delay_duration = 0.5                                # delay duration in seconds
    buffer_size = int(framerate * delay_duration)       # buffer size based on delay duration and framerate 
    buffer = RingBuffer(buffer_size)                    # allocate ring buffer 

    input_filename = input("Input filename (include .wav):  ")                      # prompt for input filename and open
    wf = openInputFile(input_filename)                                                                                             

    output_filename = removeExtensionAndAdd(input_filename, "-echo.wav")            # open output file 
    output_wf = openOutputFile(output_filename, channels, sample_width, framerate)            
 
    print("Processing audio ...")
    
    try:                                                      
        n_frames = wf.getnframes()                                           # retrieve number of frames from input file
        
        for _ in range(0, n_frames, chunk_size):                             # iterate over frames based on chunk size
            data = wf.readframes(chunk_size)                                 # read frames
            
            samples = struct.unpack(f"<{len(data)//2}h", data)               # unpack byte data into 16-bit integers
            processed_samples = []                                           # define container for all processed samples in chunk
  
            for i in range(len(samples)):                                    # process each samples
                sample = int(samples[i] * volume_factor)

                delayed_sample = buffer.popFromBuffer()                            # retrieve delayed value at index
                combined_sample = sample + int(delayed_sample * scaling_factor)    # combine delayed value with original value and adjust volume of original value
                buffer.insertToBuffer(int(combined_sample * feedback))             # insert new mixed to buffer value to be retrieved later

                combined_sample = max(-32768, min(32767, combined_sample))    # clip the combined samples to 16-bit range
                
                processed_samples.append(combined_sample)                    # append to proccess samples to output list 
                
            processed_data = struct.pack(f"<{len(processed_samples)}h", *processed_samples)  # pack processed samples
            output_wf.writeframes(processed_data)                                            # write processed audio to output file

        print("Processing complete. File saved.")
        
    except Exception as error:
        print(f"Error processing audio: {error}")                            
        
    finally:                                                                 # close input and output files
        wf.close()
        output_wf.close()

if __name__ == "__main__":
    main()
