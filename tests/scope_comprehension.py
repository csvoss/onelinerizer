x = 4

a = lambda: x

# Perhaps it once made sense to someone why c and d see the inner x
# but a and b do not.

print(''.join(
    # generator expression
    '{}{}{} {}{}{}{}\n'.format(i, j, k, a(), b(), c(), d())
    for i, b in enumerate([a, lambda: x, a])
    for j, c in enumerate([b, lambda: x, b])
    for k, d in enumerate([c, lambda: x, c])
    for x in [5]))

print(''.join(sorted({
    # set comprehension
    '{}{}{} {}{}{}{}\n'.format(i, j, k, a(), b(), c(), d())
    for i, b in enumerate([a, lambda: x, a])
    for j, c in enumerate([b, lambda: x, b])
    for k, d in enumerate([c, lambda: x, c])
    for x in [6]})))

print(''.join(sorted({
    # dict comprehension
    '{}{}{} {}{}{}{}\n'.format(i, j, k, a(), b(), c(), d()): 1
    for i, b in enumerate([a, lambda: x, a])
    for j, c in enumerate([b, lambda: x, b])
    for k, d in enumerate([c, lambda: x, c])
    for x in [7]}.keys())))

# Except in list comprehensions.

print(''.join([
    # list comprehension
    '{}{}{} {}{}{}{}\n'.format(i, j, k, a(), b(), c(), d())
    for i, b in enumerate([a, lambda: x, a])
    for j, c in enumerate([b, lambda: x, b])
    for k, d in enumerate([c, lambda: x, c])
    for x in [8]]))
