import random as rand

# Define cryptographic parameters
n = 8
Nr = 10
block_size = 16
key_length = 256


# Convert a message (string) to a binary string and give the length in digits
def convert_str_to_bin(message):
    # Check for invalid input.
    if not isinstance(message, str):
        return("Message must be a string.")

    # Conver the message to binary
    binary = ""
    for ch in message:
        binary += format(ord(ch), '08b')

    # Return the binary string
    return binary

# Convert a binary string back to a message
def convert_bin_to_str(binary):
    # Check for invalid input
    if len(binary) % 8 != 0:
        return("Enter a binary representation of an ASCII string.")
    
    # Build the message from characters in the binary array
    message = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        message += chr(int(byte, 2))

    # Return the message
    return message

# Generate a random key of length key_length
def gen_key():
    key = ""
    
    # Generate the bits of the key with a for loop
    for _ in range(key_length):
        key += str(rand.randint(0, 1))

    # Return the key
    return key

# Generate a random permutation of the first 2**n integers
def gen_perm():
    p_box = list(range(2**n))
    rand.shuffle(p_box)
    return p_box

# Generate the roundkeys from the original key
def gen_roundkey(key):
    rk = []
    seg = byte_segments(key)
    
    i = 0
    for _ in range(int(len(seg)/4)):
        rkey = []
        j = 0
        for _ in range(int(block_size/4)):
            rkey.append(seg[j+i])
            j+=1
        rk.append(rkey)
        i+=1

    return rk

# Break a binary string into segments of its bytes
def byte_segments(binary_string):
    # Split the binary string into 4-bit segments
    segments = [binary_string[i:i+4] for i in range(0, len(binary_string), 4)]
    return segments
