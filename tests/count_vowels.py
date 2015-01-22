def count_vowels(x):
    return sum([1 if i in "aeiou" else 0 for i in x.lower()])

print count_vowels("Supercalifragilisticexpialidocious!")
