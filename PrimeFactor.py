import string
import random
import sympy


class PrimeFactor:

    DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    ACCENTED_MAP = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }

    def __init__(self, seed=410, base=10, symbol_file='special_characters'):
        if not (2 <= base <= 62):
            raise ValueError("Base must be between 2 and 62.")

        self.seed = seed
        self.base = base
        self.symbol_file = symbol_file

        self.symbols = self.load_special_symbols()
        self.prime_map, self.reverse_map = self.generate_prime_map()

        self.multiplier = sympy.nextprime(max(self.prime_map.values()))

    # --------------------------------------------------
    # SYMBOL LOADER
    # --------------------------------------------------

    def load_special_symbols(self):
        try:
            with open(f"{self.symbol_file}.txt", "r", encoding="utf-8") as f:
                symbols = list(f.read().replace("\n", ""))
                return list(set(symbols))
        except FileNotFoundError:
            return list(".,!? :;()[]{}\"'-_\\/+*&%@#$^")

    # --------------------------------------------------
    # PRIME MAP
    # --------------------------------------------------

    def generate_prime_map(self):

        letters = list(string.ascii_lowercase)
        digits = list(string.digits)

        all_chars = letters + digits + self.symbols

        primes = [sympy.prime(i) for i in range(1, len(all_chars) + 1)]

        random.seed(self.seed)
        random.shuffle(all_chars)
        random.shuffle(primes)

        prime_map = {}
        reverse_map = {}

        for i, char in enumerate(all_chars):
            p = primes[i]

            prime_map[char] = p
            reverse_map[p] = char

            if char.isalpha():
                prime_map[char.upper()] = p

        for accented, base in self.ACCENTED_MAP.items():
            if base in prime_map:
                p = prime_map[base]
                prime_map[accented] = p
                prime_map[accented.upper()] = p

        return prime_map, reverse_map

    # --------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------

    def normalize_word(self, word):
        return ''.join(c for c in word if c in self.prime_map)

    # --------------------------------------------------
    # WORD → PRIME PRODUCT
    # --------------------------------------------------

    def word_to_number(self, word):

        total = 0

        for i, char in enumerate(word):
            total += self.prime_map[char] * (self.multiplier ** i)

        return total

    # --------------------------------------------------
    # NUMBER → WORD
    # --------------------------------------------------

    def number_to_word(self, number):

        letters = []

        while number > 0:

            char_prime = number % self.multiplier

            if char_prime in self.reverse_map:
                letters.append(self.reverse_map[char_prime])

            number //= self.multiplier

        return ''.join(letters)

    # --------------------------------------------------
    # BASE CONVERSION
    # --------------------------------------------------

    def to_base(self, number):

        if number == 0:
            return "0"

        result = ""

        while number > 0:
            result = self.DIGITS[number % self.base] + result
            number //= self.base

        return result

    def from_base(self, encoded):

        value = 0

        for char in encoded:

            if char not in self.DIGITS[:self.base]:
                raise ValueError("Invalid digit for base")

            value = value * self.base + self.DIGITS.index(char)

        return value

    # --------------------------------------------------
    # ENCRYPT
    # --------------------------------------------------

    def encrypt_word(self, word):

        normalized = self.normalize_word(word)

        if not normalized:
            return None

        number = self.word_to_number(normalized)

        return self.to_base(number)

    # --------------------------------------------------
    # DECRYPT
    # --------------------------------------------------

    def decrypt_word(self, word):

        number = self.from_base(word)

        return self.number_to_word(number)

    # --------------------------------------------------
    # FILE OPERATIONS
    # --------------------------------------------------

    def encrypt_file(self, input_file, output_file):

        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        words = text.split()

        encrypted = []

        for w in words:

            result = self.encrypt_word(w)

            if result:
                encrypted.append(result)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(" ".join(encrypted))

        print("Encryption complete.")
        print(f"Seed: {self.seed} | Base: {self.base}")

    def decrypt_file(self, input_file, output_file):

        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        words = text.split()

        decrypted = []

        for w in words:

            try:
                decrypted.append(self.decrypt_word(w))
            except:
                decrypted.append("[ERROR]")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(" ".join(decrypted))

        print("Decryption complete.")
        print(f"Seed: {self.seed} | Base: {self.base}")


# --------------------------------------------------
# CLI
# --------------------------------------------------

def main():

    mode = input("Mode (encrypt/decrypt): ").lower()

    try:

        seed = int(input("Seed [410]: ") or 410)
        base = int(input("Base (2-62) [10]: ") or 10)

    except:
        seed = 410
        base = 10

    pf = PrimeFactor(seed, base)

    if mode == "encrypt" or mode == "e":

        pf.encrypt_file(
            "input_text.txt",
            "encrypted_text.txt"
        )

    elif mode == "decrypt" or mode == "d":

        pf.decrypt_file(
            "input_text.txt",
            "decrypted_text.txt"
        )

    else:
        print("Invalid mode.")


if __name__ == "__main__":
    main()