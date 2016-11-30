

temp = dict.fromkeys(["a", "b", "c"], True)


print temp



# class Base(object):
#     def __init__(self):
#         self.name = None
#
#     def get_name(self):
#         return self.name
#
#     def smrdis(self):
#         print "je to: ", self.name
#
#
# class Derivate(Base):
#     def __init__(self, n1, n2):
#         super(Derivate, self).__init__()
#         self.n1 = n1
#         self.n2 = n2
#
#     def set_name(self):
#         self.name = "ahoj svete"
#
#     def get_name(self):
#         return self.name
#
#
# if __name__ == "__main__":
#     temp = Derivate(1,2)
#     temp.set_name()
#     print temp.get_name()
#     temp.smrdis()
