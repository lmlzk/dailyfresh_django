def to_tri(num):
    num = str(num)
    length = len(num)
    if length == 1:
        new_num = "00" + num
    elif length == 2:
        new_num ="0" + num
    else:
        new_num = num[:3]
    return new_num
