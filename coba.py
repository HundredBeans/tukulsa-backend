import string
import random

def randomcode(size=6, char=string.digits):
    print(''.join(random.choice(char) for _ in range(0,size)))

randomcode()