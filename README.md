One-liner
=========

Convert any Python file into a single line of code with the same functionality. No newlines allowed.

Only one semicolon allowed, and that's because I needed to invoke `from __future__ import print_function, division`.

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

Before:

    def guess_my_number(n):
        while True:
            user_input = ""
            while len(user_input)==0 or not user_input.isdigit():
                user_input = raw_input("Enter a number to guess: ")
            user_input = int(user_input)
            if user_input > n:
                print "Too big! Try again!"
            elif user_input < n:
                print "Too small! Try again!"
            else:
                print "You win!"
                return True
    guess_my_number(42)

After:

    # TODO

FAQ
---

### Oh dear God why?

Yeah. I'm sorry. But on the other hand, why not?

### Can't you use semicolons?

That would be against the spirit of this exercise. Why pass up a perfectly good excuse to abuse [lambda functions](https://docs.python.org/2/reference/expressions.html#lambda), [ternary expressions](https://docs.python.org/2/reference/expressions.html#conditional-expressions), [list comprehensions](https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions), and even the occasional [Y combinator](http://en.wikipedia.org/wiki/Fixed-point_combinator#Y_combinator)? Never pass up an opportunity to use the Y combinator.

Open Problems
-------------
* try/except/finally
* raise/assert
* classes and OOP
* global variables
* del
* exec
* with
* yield
* from foo import bar