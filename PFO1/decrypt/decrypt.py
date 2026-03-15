import string
import random
import sympy
from collections import Counter

def generate_prime_map(seed):
    """
    Generates a mapping of letters (including accented) and punctuation marks to prime
    numbers based on a fixed seed.
    """

    letters = list(string.ascii_lowercase)
    digits = list(string.digits)
    symbols = list(".,!? :;()[]{}\"'-_\\/+*&%@#$^")

    accented_letters = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }

    all_chars = letters + digits + symbols

    primes = [sympy.prime(i) for i in range(1, len(all_chars) + 1)]


    # Fix the seed to generate a consistent configuration
    random.seed(seed)
    random.shuffle(all_chars)
    random.shuffle(primes)

    # Create mapping
    prime_map = {}
    reverse_map = {}

    # Map base letters to shuffled primes
    for idx, char in enumerate(all_chars):
        p = primes[idx]
        prime_map[char] = p
        reverse_map[p] = char

        if char.isalpha():
            prime_map[char.upper()] = p

    # Add accented letters to the map
    for accented, base in accented_letters.items():
        if base in prime_map:
            p = prime_map[base]
            prime_map[accented] = p
            prime_map[accented.upper()] = p
    
    return prime_map, reverse_map

def factorize_number(number, reverse_map):
    letters = []
    multiplier = sympy.nextprime(max(reverse_map))
    while number > 0:
        char_prime = number % multiplier
        if char_prime in reverse_map:
            letters.append(reverse_map[char_prime])
        number //= multiplier
    return letters

def from_base_n(encoded_str, base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if base > 62 or base < 2:
        raise ValueError("Base must be between 2 and 62.")
    value = 0
    for char in encoded_str:
        if char not in digits[:base]:
            raise ValueError(f"Invalid character '{char}' for base {base}")
        value = value * base + digits.index(char)
    return value

def decrypt_file(input_file, output_file, seed, base):
    prime_map, reverse_map = generate_prime_map(seed)

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        encrypted_words = text.split()
        decrypted_words = []

        for word in encrypted_words:
            try:
                number = from_base_n(word, base)
                letters = factorize_number(number, reverse_map)
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