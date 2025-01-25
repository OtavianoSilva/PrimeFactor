import string
import random
import math
from collections import Counter

def generate_prime_map(seed):
    """
    Gera um mapeamento de letras (incluindo acentuadas) e sinais de pontuação para números primos
    com base em uma seed fixa. Também retorna o inverso do mapeamento (de primos para caracteres).
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

    prime_map = {}
    reverse_map = {}

    # Mapear letras básicas para primos embaralhados
    for idx, letter in enumerate(base_letters):
        prime_map[letter] = primes[idx]
        prime_map[letter.upper()] = primes[idx]  # Adiciona versão maiúscula
        reverse_map[primes[idx]] = letter

    # Adicionar letras acentuadas ao mapa
    for accented, base in accented_letters.items():
        prime_map[accented] = prime_map[base]
        prime_map[accented.upper()] = prime_map[base]
        reverse_map[prime_map[base]] = base

    # Adicionar sinais de pontuação ao mapa
    for punct, prime in punctuation_primes.items():
        prime_map[punct] = prime
        reverse_map[prime] = punct

    return prime_map, reverse_map

def factorize_number(number, prime_list):
    """
    Faz a fatoração de um número em uma lista de números primos.
    """
    factors = []
    for prime in prime_list:
        while number % prime == 0:
            factors.append(prime)
            number //= prime
        if number == 1:
            break
    return factors

def decrypt_file(input_file, output_file, seed):
    """
    Lê um arquivo de texto codificado com PrimeFactor e traduz o texto de volta ao formato original
    com base na seed fornecida.
    """
    prime_map, reverse_map = generate_prime_map(seed)
    prime_list = sorted(reverse_map.keys())  # Lista de primos em ordem crescente

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        encrypted_words = text.split()  # Divide o texto em palavras ou números codificados
        decrypted_words = []

        for word in encrypted_words:
            if word.startswith('#') and word[1:].isdigit():
                # Números, apenas remover o marcador e adicionar ao resultado
                decrypted_words.append(word[1:])
            else:
                # Palavra codificada: fatorar e traduzir
                try:
                    number = int(word)
                    factors = factorize_number(number, prime_list)
                    letters = [reverse_map[factor] for factor in factors]
                    decrypted_words.append(''.join(letters))
                except ValueError:
                    decrypted_words.append("[ERRO]")  # Marca caso ocorra um erro inesperado

        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(' '.join(decrypted_words))

        print(f"Arquivo decriptado com sucesso! Saída escrita em '{output_file}'.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Caminhos dos arquivos
input_file = 'input_text.txt'
output_file = 'decrypted_text.txt'
seed = int(input("Digite a seed para decriptar sua mensagem: "))

decrypt_file(input_file, output_file, seed)
