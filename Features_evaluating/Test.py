
class Base(object):
    def __init__(self):
        self.name = None
        self.value = None

    def get_name(self):
        return self.name

    def smrdis(self):
        print "je to: ", self.name

    def get_value(self):
        print self.value


class Derivate(Base):
    def __init__(self, n1, n2, value):
        super(Derivate, self).__init__()
        self.n1 = n1
        self.n2 = n2
        self.value = value

    def set_name(self):
        self.name = "ahoj svete"

    def get_name(self):
        return self.name


if __name__ == "__main__":
    temp = Derivate(1,2,5)
    temp.set_name()
    print temp.get_name()
    temp.smrdis()
    temp.get_value()
