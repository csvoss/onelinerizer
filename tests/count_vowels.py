def count_vowels(string):
    s = 0
    for c in string.lower():
        if c in "aeiou":
            s += 1
    return s

print count_vowels("Supercalifragilisticexpialidocious!")
