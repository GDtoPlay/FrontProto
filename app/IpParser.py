def IpParser(InStr):
    NList = InStr.split('.')
    InputCheck = "0123456789."
    if len(NList) is not 4:
        return -1
    for InChr in InStr:
        if InputCheck.find(InChr) is -1:
            return -1
    else:
        ToBin = int(NList[0]) * ((2**8)**3) + int(NList[1]) * ((2**8)**2) + int(NList[2]) * ((2**8)) +  int(NList[3])
        return ToBin
