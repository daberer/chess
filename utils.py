def loc(str):
    """
    translates string containing name of field into coordinates
    :param str: string of length two, containing char and number ("A1")
    :return:
    x and y coordinates each ranging from 0 - 700 in steps of 100.
    H1 is 0,0, A8 is 700,700
    """
    assert(len(str)==2)
    cha = list(str)[0]
    num = list(str)[1]
    return ((ord(cha)-65))*100, 800-int(num)*100

bo = {}
ob = {}
check = {}
intercept_bo = {}
for x in range(1,9):
    for y in ['A','B','C','D','E','F','G','H']:
        bo[f"{y}{x}"] = [(loc(y + str(x))), None]
        check[f"{y}{x}"] = 0
        ob[(loc(y + str(x)))] = f"{y}{x}"
        intercept_bo[f"{y}{x}"] = None

all_sprites_list = None