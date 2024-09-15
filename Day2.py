import random
while True:
    aNumberfromrandom1 = random.randint(1,10)
    aNumberfromrandom2 = random.randint(10,90)
    anApple = random.randint(aNumberfromrandom1,aNumberfromrandom2)
    anDubleapples = random.randint(aNumberfromrandom1,aNumberfromrandom2)
    useAppletorandint = anDubleapples - anApple
    aApplefromrandint = anApple + anDubleapples
    print(anApple+useAppletorandint+aApplefromrandint)
