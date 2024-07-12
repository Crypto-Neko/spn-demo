import random as rand

import random as rand

class SPN:
    l = 16
    m = 4
    Nr = 14

    def __init__(self):
        # Compute cryptographic values and apply the encryption
        self.pi = gen_perm()
        self.s_box = gen_sub()
        self.key = gen_key()
        self.rk = gen_roundkeys(key)

    # Convert a message (string) to a binary string and give the length in digits
    def convert_str_to_bin(self, message):
        # Check for invalid input.
        if not isinstance(message, str):
            return "Message must be a string."

        # Convert the message to binary
        binary = ""
        for ch in message:
            binary += format(ord(ch), '08b')

        # Return the binary string
        return binary

    # Convert a binary string back to a message
    def convert_bin_to_str(self, binary):
        # Check for invalid input
        if len(binary) % 8 != 0:
            return "Enter a binary representation of an ASCII string."
        
        # Build the message from characters in the binary array
        message = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            message += chr(int(byte, 2))

        # Return the message
        return message

    # Break a binary string into segments of its bytes
    def byte_segments(self, binary_string):
        # Split the binary string into 4-bit segments
        segments = [binary_string[i:i+4] for i in range(0, len(binary_string), 4)]
        return segments

    # Generate a random permutation of the first 2**n integers
    def gen_perm(self):
        p_box = list(range(self.l * self.m))
        rand.shuffle(p_box)
        return p_box

    # Generate a substitution box
    def gen_sub(self):
        s_box = list(range(self.l))
        rand.shuffle(s_box)
        return s_box

    # Generate a random key of length key_length
    def gen_key(self):
        key = ""
        
        # Generate the bits of the key with a for loop
        for _ in range(256):
            key += str(rand.randint(0, 1))

        # Return the key
        return key

    # Generate the roundkeys from the original key
    def gen_roundkeys(self, key):
        rk = []
        seg = self.byte_segments(key)
        
        i = 0
        for _ in range(self.Nr):
            rkey = []
            j = 0
            for _ in range(int(4)):
                rkey.append(seg[j+i])
                j += 1
            rk.append(rkey)
            i += 1

        return rk

    # Apply the substitution
    def apply_sub(self, block):
        new_block = []
        for byte in block:
            new_byte = convert_str_to_bin(chr(self.s_box[int(byte, 2)]))
            new_block.append(new_byte)
        return new_block
