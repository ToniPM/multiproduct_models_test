from State import Move


class ProductMove(Move):
    def __init__(self, i1, i2):
        self.i1 = i1
        self.i2 = i2

    def __repr__(self):
        return "ProductMove({},{})".format(self.i1, self.i2)
