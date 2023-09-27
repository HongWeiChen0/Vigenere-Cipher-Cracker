# frequency of each letter in English for frequency analysis
frequency = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02360,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}


# get distribution from letter count
def getDistribution(letter_count):
    distribution = {}
    total = 0
    for val in letter_count.values():
        total += val
    for char, count in letter_count.items():
        distribution[char] = count / total
    return distribution


# calculate the mean squared error for a distribution
def getMSE(cipher_distribution):
    squared_differences = 0
    for key in frequency:
        squared_differences += (frequency[key] - cipher_distribution[key]) ** 2
    return squared_differences / len(frequency)


# shift every character in a string by certain amount
def shift(text, amount):
    shifted = ""
    for char in text:
        shifted_char = chr(
            ((ord(char) - ord('A') - amount) % 26) + ord('A'))
        shifted += shifted_char
    return shifted


# decrypt function given key and ciphertext
def decrypt(ciphertext, key):
    result = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            if char.islower():
                result += chr(ord('a') + (ord(char) - ord('a') - shift) % 26)
            else:
                result += chr(ord('A') + (ord(char) - ord('A') - shift) % 26)
            key_index += 1
        else:
            result += char
    return result


def crack(orig_ciphertext, key_length):
    key = ""
    ciphertext = ''.join(
        char.upper() for char in orig_ciphertext if char.isalpha())
    # crack key letter by letter
    for i in range(key_length):
        # get every ith letter, corresponding to the characters shifted by the ith key
        ith_letters = ""
        for j in range(i, len(ciphertext), key_length):
            ith_letters += ciphertext[j]

        # try every shift from 0 to 25 and see which distribution matches the best
        best_mse = float('inf')
        best_char = ''
        for shift_amount in range(26):
            shifted_text = shift(ith_letters, shift_amount)
            letter_count = {
                chr(letter): 0 for letter in range(ord('A'), ord('Z')+1)}
            for char in shifted_text:
                letter_count[char] += 1
            distribution = getDistribution(letter_count)
            mse = getMSE(distribution)
            if mse < best_mse:
                best_mse = mse
                best_char = chr(ord('A') + shift_amount)
        key += best_char
    return (key, decrypt(orig_ciphertext, key))


ciphertext = input("Enter ciphertext: ")
length = int(input("Enter key length: "))
key, decrypted = crack(ciphertext, length)
print(key)
print(decrypted)
