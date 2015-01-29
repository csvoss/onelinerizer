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
