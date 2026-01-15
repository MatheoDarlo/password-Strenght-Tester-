import re
import unicodedata
import random
from .config import DICTIONARY, BREACHED_PASSWORDS, SUGGEST_WORDS

def leet_substitutions(word):
    subs = [
        ('4', 'a'), ('@', 'a'),
        ('3', 'e'),
        ('1', 'i'), ('!', 'i'),
        ('0', 'o'),
        ('$', 's'),
        ('7', 't'),
        ('5', 's'),
        ('8', 'b'),
    ]
    for leet, char in subs:
        word = word.replace(leet, char)
    return word

def contains_dictionary_word(password):
    lower = password.lower()
    leet_lower = leet_substitutions(lower)
    return any(word for word in DICTIONARY if len(word) > 2 and (word in lower or word in leet_lower))

def is_breached(password):
    return password.lower() in BREACHED_PASSWORDS

def has_repeated_chars(password, min_repeat=4):
    count = 1
    last = ''
    for c in password:
        if c == last:
            count += 1
            if count >= min_repeat:
                return True
        else:
            count = 1
            last = c
    return False

def is_slight_variation(password, words):
    cleaned = ''.join([c for c in password.lower() if c.isalpha()])
    return any(word for word in words if len(word) > 2 and word in cleaned)

def has_sequence(pw):
    pw = pw.lower()
    for seq in [
        '0123456789', 'abcdefghijklmnopqrstuvwxyz', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
        '0987654321', 'zyxwvutsrqponmlkjihgfedcba', 'poiuytrewq', 'lkjhgfdsa', 'mnbvcxz'
    ]:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in pw:
                return True
    return False

def generate_strong_password(num_words=4):
    words = random.sample(SUGGEST_WORDS, num_words)
    sep = random.choice(['-', '_', '.', '~'])
    number = str(random.randint(10, 99))
    symbol = random.choice(['!', '@', '#', '$', '%', '&', '*'])
    passphrase = sep.join(words) + number + symbol
    return passphrase
