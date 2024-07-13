# SPN Demo

This is a basic implementation of a Substitution-Permutation Network.
It generates a key, a substitution box, and a permutation box, then generating roundkeys from the original key and applying them long with the substitution and permutation to encrypt a message of plaintext.
It took me a few days to create and now it's complete. With the parameters I used in the code, it can only encrypt messages two characters of length or smaller, but it could be extended beyond this.
This was a warm-up for my next project, which will be to create a program capable of formatting and encrypting a block device with AES.
