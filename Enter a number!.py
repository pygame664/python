numlist = list()
while True :
    inp = input('Enter a number：')
    if inp == 'ok' :
        break
    value = float(inp)
    numlist.append(value)


average = sum(numlist)
d = round(average, 0)
print('equals:', d)
