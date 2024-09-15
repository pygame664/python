try:
    import random
    words = ['chicken','dog','cat','mouse','frog']
    guessTimes = 14
    guessedLetters = ""
    disPlayword = ""


    def pickword():
        return random.choice(words)


    def play():
        word = pickword()
        while True:
            guess = getGuess(word)
            if processGuess(guess, word):
                print('You win!')
                break
                if guessTime == 0:
                    print('Game over!')
                    print('The word was: ' + word)
                    break


    def getGuess(word):
        print(WordWithBlanks(word))
        print('Guess Times Remaining: ' + str(guessTimes))
        guess = raw_input(' Guess a letter?')
        return guess


    def processGuess(guess, word):
        global guessTimes
        global guessedLetters
        guessTimes = guessTimes - 1
        guessedLetters = guessedLetters + guess
    

    for letter in words:
        if guessedLetters.find(letter) > -1:
            disPlayword = disPlayword + letter
        else:
            disPlayword = disPlayword + '-'
    print(disPlayword)


    play()

except IndexError:
    print('somthingworng!')
