import random as rand

class SPN:
    l = 4
    m = 4
    Nr = 5

    def __init__(self):
        # Compute cryptographic values and apply the encryption
        self.pi = self.gen_perm()
        self.s_box = self.gen_sub()
        self.key = self.gen_key()
        self.rk = self.gen_roundkeys(self.key)

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
        
        for i in range(len(p_box)):
            p_box[i] = format(p_box[i], '04b')
        
        p_box_inv = [0] * len(p_box)
        for i, v in enumerate(p_box):
            p_box_inv[int(v, 2)] = format(i, '04b')
        self.pi_inv = p_box_inv

        return p_box

    # Generate a substitution box
    def gen_sub(self):
        s_box = list(range(2**self.l))
        rand.shuffle(s_box)

        for i in range(len(s_box)):
            s_box[i] = format(s_box[i], '04b')

        s_box_inv = [0] * len(s_box)
        for i, v in enumerate(s_box):
            s_box_inv[int(v, 2)] = format(i, '04b')
        self.s_box_inv = s_box_inv

        return s_box

    # Generate a random key of length key_length
    def gen_key(self):
        key = ""
        
        # Generate the bits of the key with a for loop
        for _ in range(32):
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
        sub = []
        for byte in block:
            sub.append(self.s_box[int(byte, 2)])
        return sub

    # Apply the inverse substitution
    def apply_sub_inv(self, block):
        sub = []
        for byte in block:
            sub.append(self.s_box_inv[int(byte, 2)])
        return sub

    # Apply the permutation
    def apply_pi(self, state):
        new_state = []
        for byte in state:
            new_byte = str(self.pi[int(byte, 2)])
            new_state.append(new_byte)
        return new_state

    # Apply the inverse permutation
    def apply_pi_inv(self, state):
        new_state = []
        for byte in state:
            new_byte = str(self.pi_inv[int(byte, 2)])
            new_state.append(new_byte)
        return new_state

    # Oplus the roundkey with the current byte
    def add_round_key(self, state, rk):
        new_state = []
        rk = rk[:len(state)]
        for block, key in zip(state, rk):
            new_block = ""
            for b, k in zip(block, key):
                new_byte = ""
                for bit_b, bit_k in zip(b, k):
                    new_byte += str((int(bit_b) + int(bit_k)) % 2)
                new_block += new_byte
            new_state.append(new_block)
        return new_state

    # Perform the encryption
    def spn_encrypt(self, plaintext):
        state = self.convert_str_to_bin(plaintext)
        state = self.byte_segments(state)

        for i in range(self.Nr - 1):
            state = self.add_round_key(state, self.rk[i])
            state = self.apply_sub(state)
            state = self.apply_pi(state)

        state = self.add_round_key(state, self.rk[self.Nr - 1])
        ciphertext = ''.join(state)
        
        ciphertext_str = ""
        for byte in ciphertext:
            for bit in byte:
                ciphertext_str += bit
        ciphertext_str = self.convert_bin_to_str(ciphertext_str)
        
        return ciphertext_str

    # Perform the decryption
    def spn_decrypt(self, ciphertext):
        state = self.convert_str_to_bin(ciphertext)
        state = self.byte_segments(state)

        # Apply the final round key first
        state = self.add_round_key(state, self.rk[self.Nr - 1])

        for i in range(self.Nr - 2, -1, -1):
            state = self.apply_pi_inv(state)
            state = self.apply_sub_inv(state)
            state = self.add_round_key(state, self.rk[i])

        plaintext = ''.join(state)

        plaintext_str = ""
        for byte in plaintext:
            for bit in byte:
                plaintext_str += bit
        plaintext_str = self.convert_bin_to_str(plaintext_str)

        return plaintext_str


# Example usage
spn = SPN()
print("Original message: c")
cipher_text = spn.spn_encrypt("c")
print(f"Cipher Text: {cipher_text}")
decrypt = spn.spn_decrypt(cipher_text)
print(f"Decrypted Text: {decrypt}")

