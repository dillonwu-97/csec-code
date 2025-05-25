from string import ascii_lowercase
from secret import FLAG, KEY
import random
import re

random.seed(KEY)

text = re.sub(r'[^a-z ]', r'?', open('zoomer.txt').read().lower())

i = random.randint(0, len(text))
text = text[:i] + FLAG + text[i:]

emojis = list(open('emojis.txt').read())
[random.shuffle(emojis) for _ in range(10)]     # Shuffle 10 times to make sure its random

# Add some decoys for confusion
for _ in range(500):
    i = random.randint(0, len(text))
    text = text[:i] + emojis.pop() + text[i:]

# Encrypt with emojis
for c in ascii_lowercase + ' ?':

    # replace character with a chunk of emojis
    # must be of length 2->9
    text = text.replace(c, ''.join(emojis.pop() for _ in range(random.randint(2,9))))

# frequency attack?
open('zoomer.emoji', 'w').write(text)