import string
import random
import unicodedata

def generate_prime_map(seed):
    """
    Gera um mapeamento de letras (incluindo acentuadas) e sinais de pontuação para números primos
    com base em uma seed fixa.
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

    # Fixar a seed para gerar uma configuração consistente
    random.seed(seed)
    random.shuffle(base_letters)
    random.shuffle(primes)

    # Criar mapeamento
    prime_map = {}

    # Mapear letras básicas para primos embaralhados
    for idx, letter in enumerate(base_letters):
        prime_map[letter] = primes[idx]
        prime_map[letter.upper()] = primes[idx]  # Adiciona versão maiúscula

    # Adicionar letras acentuadas ao mapa
    for accented, base in accented_letters.items():
        prime_map[accented] = prime_map[base]
        prime_map[accented.upper()] = prime_map[base]

    # Adicionar sinais de pontuação ao mapa
    prime_map.update(punctuation_primes)

    return prime_map

def normalize_word(word):
    """
    Remove caracteres não suportados e mantém pontuação e letras.
    """
    word = ''.join(
        char for char in word
        if char.isalnum() or char in "áàâãäéèêëíìîïóòôõöúùûüçñÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ.!,?:;()[]{}\"'-_/*+&%@#$"
    )
    return word

def word_to_prime_product(word, prime_map):
    """
    Converte uma palavra em um número pela multiplicação dos primos de cada caractere.
    """
    product = 1
    for char in word:
        if char in prime_map:  # Ignorar caracteres que não estejam no mapa
            product *= prime_map[char]
    return product

def to_base_n(number, base):
    """
    Converte um número inteiro para uma string em base N (até base 32).
    Usa dígitos 0-9 e letras A-V.
    """
    if number == 0:
        return "0"

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if base > 32 or base < 2:
        raise ValueError("Base deve estar entre 2 e 32.")

    result = ''
    while number > 0:
        result = digits[number % base] + result
        number //= base
    return result

def encrypt_file(input_file, output_file, seed, base):
    """
    Lê um arquivo de texto e converte cada palavra para um número baseado em primos,
    convertendo esse número para a base escolhida, mantendo números intactos precedidos por #.
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
                encrypted_number = word_to_prime_product(normalized_word, prime_map)
                encrypted_base_n = to_base_n(encrypted_number, base)
                encrypted_words.append(encrypted_base_n)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(' '.join(encrypted_words))

        print(f"Arquivo encriptado com sucesso! Saída escrita em '{output_file}'.")
        print(f"Seed utilizada: {seed} | Base utilizada: {base}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Caminhos dos arquivos
input_file = 'input_text.txt'
output_file = 'encrypted_text.txt'
seed = int(input("Digite a seed para encriptar sua mensagem: ") or 410)

try:
    base = int(input("Digite a base de numeração (2 a 32): ") or 10)
    if not (2 <= base <= 32):
        raise ValueError
except ValueError:
    print("Base inválida. Usando base 10 por padrão.")
    base = 10

encrypt_file(input_file, output_file, seed, base)