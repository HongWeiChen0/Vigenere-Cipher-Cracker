def encrypt(plaintext, key):
    result = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            if char.islower():
                result += chr(ord('a') + (ord(char) - ord('a') + shift) % 26)
            else:
                result += chr(ord('A') + (ord(char) - ord('A') + shift) % 26)
            key_index += 1
        else:
            result += char
    return result


plaintext = input("Enter plaintext: ")
key = input("Enter key: ")
print(encrypt(plaintext, key))
