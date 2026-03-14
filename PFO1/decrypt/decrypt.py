import string
import random
import math
from collections import Counter

def generate_prime_map(seed):
    """
    Generates a mapping of letters (including accented) and punctuation marks to prime
    numbers based on a fixed seed. It also returns the inverse of the mapping (from
    primes to characters)
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    punctuation_primes = {
        '.': 103, ',': 107, '!': 109, '?': 113, ':': 127, ';': 131,
        '(': 137, ')': 139, '[': 149, ']': 151, '{': 157, '}': 163,
        '"': 167, "'": 173, '-': 179, '_': 181, '/': 191, '\\': 193,
        '+': 197, '=': 199, '*': 211, '&': 223, '%': 227, '@': 229, '#': 233, '$': 239
    }

    base_letters = list(string.ascii_lowercase)
    accented_letters = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }

    random.seed(seed)
    random.shuffle(base_letters)
    random.shuffle(primes)

    prime_map = {}
    reverse_map = {}

    for idx, letter in enumerate(base_letters):
        prime_map[letter] = primes[idx]
        prime_map[letter.upper()] = primes[idx]
        reverse_map[primes[idx]] = letter

    for accented, base in accented_letters.items():
        prime_map[accented] = prime_map[base]
        prime_map[accented.upper()] = prime_map[base]
        reverse_map[prime_map[base]] = base

    for punct, prime in punctuation_primes.items():
        prime_map[punct] = prime
        reverse_map[prime] = punct

    return prime_map, reverse_map

def factorize_number(number, prime_list):
    """
    Factors a number from a list of prime numbers
    """
    factors = []
    for prime in prime_list:
        while number % prime == 0:
            factors.append(prime)
            number //= prime
        if number == 1:
            break
    return factors

def from_base_n(encoded_str, base):
    """
    Converts a string representing a number in base N to base 10.
    Supports up to base 62.
    """
    # Mesma sequência usada na criptografia
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    if base > 62 or base < 2:
        raise ValueError("Base must be between 2 and 62.")

    value = 0
    for char in encoded_str:
        # Removido o .upper() para manter a sensibilidade entre maiúsculas e minúsculas
        if char not in digits[:base]:
            raise ValueError(f"Invalid character '{char}' for base {base}")
        value = value * base + digits.index(char)
    return value

def decrypt_file(input_file, output_file, seed, base):
    """
    Reads a text file encoded with PrimeFactor and translates the text back to the
    original format based on the seed and base provided.
    """
    prime_map, reverse_map = generate_prime_map(seed)
    prime_list = sorted(reverse_map.keys())

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        encrypted_words = text.split()
        decrypted_words = []

        for word in encrypted_words:
            if word.startswith('#') and word[1:].isdigit():
                decrypted_words.append(word[1:])
            else:
                try:
                    number = from_base_n(word, base)
                    factors = factorize_number(number, prime_list)
                    letters = [reverse_map[factor] for factor in factors]
                    decrypted_words.append(''.join(letters))
                except Exception as e:
                    decrypted_words.append("[ERROR]")

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(' '.join(decrypted_words))

        print(f"File decrypted successfully! Output written to '{output_file}'.")
        print(f"Seed used: {seed} | Base Used: {base}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
input_file = 'input_text.txt'
output_file = 'decrypted_text.txt'

try:
    seed_input = input("Enter the seed to decrypt your message (default 410): ")
    seed = int(seed_input) if seed_input else 410
    
    base_input = input("Enter the base used for encryption (2 to 62) [Default 10]: ")
    base = int(base_input) if base_input else 10
    
    if not (2 <= base <= 62):
        raise ValueError
except ValueError:
    print("Invalid base or seed. Using default values (Seed: 410, Base: 10).")
    seed = 410
    base = 10

decrypt_file(input_file, output_file, seed, base)