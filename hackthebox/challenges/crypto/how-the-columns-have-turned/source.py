import os


with open('super_secret_messages.txt', 'r') as f:
    SUPER_SECRET_MESSAGES = [msg.strip() for msg in f.readlines()]


# Derive key by enumerating the letters in the key
# 
def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        # for each of the previous characters
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key


def transpose(array):
    return [row for row in map(list, zip(*array))]


def flatten(array):
    return "".join([i for sub in array for i in sub])


# derive the key using the plaintext and some key value as well 
# the key is a string? since we are getting the width
# then generate blocks to encrypt by breaking up the plaintext
# for each character in the key, we take the block for that index and then reverse the order of the characters?
# Then we flatten the ciphertext

# Observation: the random number is just the same number each time
def twistedColumnarEncrypt(pt, key):
    derived_key = deriveKey(key)

    width = len(key)

    blocks = [pt[i:i + width] for i in range(0, len(pt), width)]
    blocks = transpose(blocks) # transpose again to reverse this operation

    # .index() returns the position of the value
    # So derived_key.index(7) gives the index of value 7
    # length of each block is 7

    ct = [blocks[derived_key.index(i + 1)][::-1] for i in range(width)] # this should give an out of range error with the key that I have
    ct = flatten(ct)
    return ct


class PRNG:
    def __init__(self, seed):

        # huh???
        self.p = 0x2ea250216d705
        self.a = self.p
        self.b = int.from_bytes(os.urandom(16), 'big')
        self.rn = seed

    # next value is just the same each time I think, so b is the key??
    def next(self):
        # self.rn is just b?
        self.rn = ((self.a * self.rn) + self.b) % self.p
        return self.rn


def main():
    seed = int.from_bytes(os.urandom(16), 'big') # Get a seed value
    rng = PRNG(seed) # Get some initial random value using the seed

    cts = ""

    # We also have the last key 
    for message in SUPER_SECRET_MESSAGES: # For each message, generate a new key and encrypt the message using the key

        key = str(rng.next())
        ct = twistedColumnarEncrypt(message, key) # encrypted using the key 148823505998502
        cts += ct + "\n"

    with open('encrypted_messages.txt', 'w') as f:
        f.write(cts)

    dialog = "Miyuki says:\n"
    dialog += "Klaus it's your time to sign!\n"
    dialog += "All we have is the last key of this wierd encryption scheme.\n"
    dialog += "Please do your magic, we need to gather more information if we want to defeat Draeger.\n"
    dialog += f"The key is: {str(key)}\n"

    with open('dialog.txt', 'w') as f:
        f.write(dialog)


if __name__ == '__main__':
    main()
