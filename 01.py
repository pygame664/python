try:
    import random
    while True:
        randomNumber1 = random.randint(1,6)
        randomNumber2 = random.randint(1,6)


        total = randomNumber1 + randomNumber2


        if randomNumber1 == randomNumber2:
            print('double')
            if randomNumber1 == 6:
                break
        else:
            if total > 8:
                print('big')
            elif total > 4:
                print('notbad')
            else:
                print('small')
except IndexError:
    print('somthingworng!')
