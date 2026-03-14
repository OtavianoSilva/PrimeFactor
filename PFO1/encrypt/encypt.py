import string
import random
import unicodedata

def generate_prime_map(seed):
    """
    Generates a mapping of letters (including accented) and punctuation marks to prime
    numbers based on a fixed seed.
    """
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
        157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 
        239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 
        331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409
    ]

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

    # Fix the seed to generate a consistent configuration
    random.seed(seed)
    random.shuffle(all_chars)
    random.shuffle(primes)

    # Create mapping
    prime_map = {}

    # Map base letters to shuffled primes
    for idx, char in enumerate(all_chars):
        p = primes[idx]
        prime_map[char] = p

        if char.isalpha():
            prime_map[char.upper()] = p

    # Add accented letters to the map
    for accented, base in accented_letters.items():
        if base in prime_map:
            p = prime_map[base]
            prime_map[accented] = p
            prime_map[accented.upper()] = p

    return prime_map

def normalize_word(word):
    """
    Removes unsupported characters and keeps punctuation and letters.
    """
    allowed_chars = "áàâãäéèêëíìîïóòôõöúùûüçñÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ.!,?:;()[]{}\"'-_/*+&%@#$"
    word = ''.join(
        char for char in word
        if char.isalnum() or char in allowed_chars
    )
    return word

def word_to_prime_product(word, prime_map):
    """
    Converts a word into a number by multiplying the primes of each character and
    their relative position
    """
    total_value = 0
    multiplier = 419 # Needs to be a prime out of prime_map and greater than all of them
    for i, char in enumerate(word):
        if char in prime_map:  # Ignore characters not in the map
            # It creates the relationship between numbers and their relative position
            total_value += prime_map[char] * (multiplier ** i)
    return total_value

def to_base_n(number, base):
    """
    Converts an integer to a string in base N (up to base 62).
    Uses digits 0-9, A-Z, and a-z following ASCII order.
    """
    if number == 0:
        return "0"

    # Sequência seguindo a ordem da tabela ASCII: 0-9, A-Z, a-z
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    if base > 62 or base < 2:
        raise ValueError("Base must be between 2 and 62.")

    result = ''
    while number > 0:
        result = digits[number % base] + result
        number //= base
    return result

def encrypt_file(input_file, output_file, seed, base):
    """
    Reads a text file and converts each word to a prime-based number,
    converting that number to the chosen base, keeping numbers intact preceded by #.
    """
    prime_map = generate_prime_map(seed)

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        words = text.split()
        encrypted_words = []

        for word in words:
            if word.isdigit():
                encrypted_words.append(f"#{word}")
            else:
                normalized_word = normalize_word(word)
                if not normalized_word:  # Evita erro de palavra vazia
                    continue
                encrypted_number = word_to_prime_product(normalized_word, prime_map)
                encrypted_base_n = to_base_n(encrypted_number, base)
                encrypted_words.append(encrypted_base_n)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(' '.join(encrypted_words))

        print(f"File encrypted successfully! Output written to '{output_file}'.")
        print(f"Seed used: {seed} | Base used: {base}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
input_file = 'input_text.txt'
output_file = 'encrypted_text.txt'

try:
    seed_input = input("Enter the seed to encrypt your message (default 410): ")
    seed = int(seed_input) if seed_input else 410
    
    # Atualizado para pedir até a base 62
    base_input = input("Enter the numbering base (2 to 62) [default 10]: ")
    base = int(base_input) if base_input else 10
    
    if not (2 <= base <= 62):
        raise ValueError
except ValueError:
    print("Invalid input. Using default values (Seed: 410, Base: 10).")
    seed = 410
    base = 10

encrypt_file(input_file, output_file, seed, base)