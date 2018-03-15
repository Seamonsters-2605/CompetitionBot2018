import seamonsters as sea
def LeftPause():
    table = sea.getNum()
    yield from sea.wait(int(table['lpause'])*50)

def RightPause():
    table = sea.getNum()
    yield from sea.wait(int(table['rpause'])*50)