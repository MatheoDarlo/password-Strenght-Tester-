import unicodedata
import logging
from .utils import (
    contains_dictionary_word, is_breached, has_repeated_chars, is_slight_variation, has_sequence
)
from .config import DICTIONARY

def evaluate_password(password):
    score = 0
    tips = []
    password_norm = unicodedata.normalize('NFKC', password)
    has_length = len(password_norm) >= 15
    has_upper = any(c.isupper() for c in password_norm)
    has_lower = any(c.islower() for c in password_norm)
    has_number = any(c.isdigit() for c in password_norm)
    has_symbol = any(not c.isalnum() for c in password_norm)
    common_pattern = contains_dictionary_word(password_norm)
    sequence_pattern = has_sequence(password_norm)
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'poiuy', 'lkjhg', 'mnbvc']
    keyboard_pattern = any(kp in password_norm.lower() for kp in keyboard_patterns)
    breached_pattern = is_breached(password_norm)
    repeated_pattern = has_repeated_chars(password_norm)
    variation_pattern = is_slight_variation(password_norm, DICTIONARY)

    if has_length:
        score += 1
    else:
        tips.append('Use at least 15 characters for best security.')
    if has_upper:
        score += 1
    else:
        tips.append('Add uppercase letters.')
    if has_lower:
        score += 1
    else:
        tips.append('Add lowercase letters.')
    if has_number:
        score += 1
    else:
        tips.append('Add numbers.')
    if has_symbol:
        score += 1
    else:
        tips.append('Add special characters.')
    if breached_pattern:
        score = max(score - 3, 0)
        tips.append('This password has been found in data breaches. Never use it!')
    if repeated_pattern:
        score = max(score - 2, 0)
        tips.append('Avoid repeated characters (e.g., "aaaa", "1111").')
    if variation_pattern:
        score = max(score - 2, 0)
        tips.append('Avoid slight variations of common words (e.g., "password1!").')
    if common_pattern or sequence_pattern or keyboard_pattern:
        score = max(score - 2, 0)
        tips.append('Avoid common words, names, patterns, or keyboard sequences.')

    # Log weakness types (never the password)
    weakness_types = []
    if breached_pattern:
        weakness_types.append('breached')
    if repeated_pattern:
        weakness_types.append('repeated')
    if variation_pattern:
        weakness_types.append('variation')
    if common_pattern:
        weakness_types.append('dictionary')
    if sequence_pattern:
        weakness_types.append('sequence')
    if keyboard_pattern:
        weakness_types.append('keyboard')
    if weakness_types:
        logging.info(f'Weaknesses detected: {", ".join(weakness_types)}')

    # Count how many positive conditions are met
    conditions_met = sum([has_length, has_upper, has_lower, has_number, has_symbol])
    # Only penalize for breached or slight variation for 'Strong'
    if conditions_met == 5 and not (breached_pattern or variation_pattern):
        strength = 'Strong'
    elif conditions_met >= 3 and not breached_pattern:
        strength = 'Medium'
    else:
        strength = 'Weak'

    return {
        'strength': strength,
        'tips': tips,
        'indicators': {
            'hasLength': has_length,
            'hasUpper': has_upper,
            'hasLower': has_lower,
            'hasNumber': has_number,
            'hasSymbol': has_symbol
        },
        'commonPattern': common_pattern
    }
