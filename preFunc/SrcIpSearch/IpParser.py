def IpParser(InStr):
    NList = InStr.split('.')
    InputCheck = "0123456789."
    if Nlist.len != 4:
        return -1
    for InChr in InStr:
        if InputCheck.find(InChr) is -1:
            return -1
    else:
        ToBin = Nlist[0] * ((2**8)**3) + Nlist[1] * ((2**8)**2) + Nlist[2] * ((2**8)) +  Nlist[3]
        return ToBin
