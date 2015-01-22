One-liner
=========

Convert any Python file into a single line of code with the same functionality.

Installation and Usage
----------------------

    git clone https://github.com/csvoss/oneliner
    python oneliner/main.py name_of_target_file.py

Examples
--------

Before:

    x = 3
    y = 4
    print (x < y < 5)

After:

    (lambda x: (lambda y: print(x<y<5))(4))(3)


FAQ
---

### Oh dear God why?

Yeah. I'm sorry. But on the other hand, why not?

But on the other hand, why not?

### Can't you use semicolons?

That would be against the spirit of this exercise. Why pass up a perfectly good excuse to abuse lambda functions, ternary expressions, list comprehensions, and even the occasional Y combinator? Never pass up an opportunity to use the Y combinator.

Open Problems
-------------
* try/except/finally
* raise/assert