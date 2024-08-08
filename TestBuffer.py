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
    This helper function prints the value in the buffer, the size of the buffer and the indices 
    that head and tail are pointing to. It is a debugging function. 
    """
def printBuffer(buffer):
    print(f"Buffer: {buffer.data}")
    print(f"Head: {buffer.head}, Tail: {buffer.tail}, Count: {buffer.count}")
    print()

"""
Run Main to See Tests
"""
def main():
    print("Test running")
    ring_buffer = RingBuffer(5)

    print("initial buffer state:")
    printBuffer(ring_buffer)

    print("Inserting 4 values...")
    ring_buffer.insertToBuffer(4)
    ring_buffer.insertToBuffer(5)
    ring_buffer.insertToBuffer(11)
    ring_buffer.insertToBuffer(-5)
    printBuffer(ring_buffer)

    print("Popping buffer...")
    popped_value = ring_buffer.popFromBuffer()
    print(f"Popped Value: {popped_value}")
    printBuffer(ring_buffer)

    print("Inserting values 1 and 8")
    ring_buffer.insertToBuffer(1)
    ring_buffer.insertToBuffer(8)
    printBuffer(ring_buffer)

    print("Inserting 6 ... should fail... no pointers should move")
    ring_buffer.insertToBuffer(6)
    printBuffer(ring_buffer)

    print("Inserting 6 ... using overwrite function...")
    ring_buffer.insertToBufferOver(6)
    printBuffer(ring_buffer)

    print("Emptying buffer...")
    while ring_buffer.count > 0:
        ring_buffer.popFromBuffer()

    print("Buffer empty.")
    printBuffer(ring_buffer)

if __name__ == "__main__":
    main()
