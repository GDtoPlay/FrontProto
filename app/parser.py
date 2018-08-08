def parser(string):
    Parsed_List = []
    NList = string.split(' ')
    current_int = 0
    counter = 8
    for ch in NList:
        if counter is 8:
            current_int = current_int + int(ch, 16) * ((2**8)**7)
            counter = counter -1
        elif counter is 7:
            current_int = current_int + int(ch, 16) * ((2**8)**6)
            counter = counter -1
        elif counter is 6:
            current_int = current_int + int(ch, 16) * ((2**8)**5)
            counter = counter -1
        elif counter is 5:
            current_int = current_int + int(ch, 16) * ((2**8)**4)
            counter = counter -1
        elif counter is 4:
            current_int = current_int + int(ch, 16) * ((2**8)**3)
            counter = counter -1
        elif counter is 3:
            current_int = current_int + int(ch, 16) * ((2**8)**2)
            counter = counter -1
        elif counter is 2:
            current_int = current_int + int(ch, 16) * ((2**8))
            counter = counter -1
        elif counter is 1:
            current_int = current_int + int(ch, 16)
            Parsed_List.append(current_int)
            current_int = 0
            counter = 8
    if current_int is not 0:
        Parsed_List.append(current_int)

    return Parsed_List
