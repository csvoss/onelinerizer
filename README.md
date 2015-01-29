One-liner
=========

Convert any Python file into a single line of code with the same functionality. No newlines allowed. No semicolons allowed, either.

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

    (lambda __builtin__: (lambda __print, __y, d: [[__print(d.x<d.y<5) for d.y in [(4)]][0] for d.x in [(3)]][0])(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))

That line looks complicated, because we need some tricks to import the print function and to support some other complicated features. For a program as simple as this one, you can think of it as working this way:

     (lambda x: (lambda y: print(x<y<5))(4))(3)

Before:

    def f(x):
        return x+5
    print f(13)

After:

    (lambda __builtin__: (lambda __print, __y, d: [__print(d.f(13)) for d.f in [(lambda x:[(d.x+5) for d.x in [(x)]][0])]][0])(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))

...or, if you want to think about something more simplified:

    (lambda f: print(f(13)))(lambda x: x+5)

Before:

    def guess_my_number(n):
        while True:
            user_input = raw_input("Enter a positive integer to guess: ")
            if len(user_input)==0 or not user_input.isdigit():
                print "Not a positive integer!"
            else:
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

    (lambda __builtin__: (lambda __print, __y, d: [(lambda ___: None)(d.guess_my_number(42)) for d.guess_my_number in [(lambda n:[(__y(lambda __this: (lambda d: (lambda __after: [(lambda __after: (lambda ___: __after(d))(__print('Not a positive integer!')) if (d.len(d.user_input)==0 or (not d.user_input.isdigit())) else [(lambda __after: (lambda ___: __after(d))(__print('Too big! Try again!')) if d.user_input>d.n else (lambda __after: (lambda ___: __after(d))(__print('Too small! Try again!')) if d.user_input<d.n else (lambda ___: d.True)(__print('You win!')))(lambda d: __after(d)))(lambda d: __after(d)) for d.user_input in [(d.int(d.user_input))]][0])(lambda d: __this(d)) for d.user_input in [(d.raw_input('Enter a positive integer to guess: '))]][0] if d.True else __after(d))(lambda d: None))))(d) for d.n in [(n)]][0])]][0])(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))

FAQ
---

### Oh dear God why?

Yeah. I'm sorry. But on the other hand, why not?

### Can't you use semicolons?

That would be against the spirit of this exercise. Why pass up a perfectly good excuse to abuse [lambda functions](https://docs.python.org/2/reference/expressions.html#lambda), [ternary expressions](https://docs.python.org/2/reference/expressions.html#conditional-expressions), [list comprehensions](https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions), and even the occasional [Y combinator](http://en.wikipedia.org/wiki/Fixed-point_combinator#Y_combinator)? Never pass up an opportunity to use the Y combinator.

Analysis
--------
### Space

O(n). No code is ever duplicated, so the one-lined code produced is linear in the size of the input code.

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