def binToAsc(InStr):
    NSTR = ""
    for InChar in InStr:
        if int(hex(ord(InChar)), 16) > 126 or int(hex(ord(InChar)), 16) < 64:
            NSTR = NSTR + " "
        else:
            NSTR = NSTR + chr(int(hex(ord(InChar)), 16))
    return NSTR
